import asyncio
import reflex as rx
from .config import settings
import os
import secrets
import base64
import time
import json
import httpx
from typing import Optional, List
from datetime import datetime, timedelta
from urllib.parse import urlparse

# Set environment variables before importing GoogleAuthState
os.environ["GOOGLE_CLIENT_ID"] = settings.google_client_id
os.environ["GOOGLE_CLIENT_SECRET"] = settings.google_client_secret

from reflex_google_auth import GoogleAuthState


import base58
from .core import encryption, encoding, redis_client
from .database import SessionLocal
from .models import User

def _get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        return None


def _decode_jwt_payload(token: str) -> dict:
    parts = token.split(".")
    if len(parts) < 2:
        return {}
    payload = parts[1]
    payload += "=" * (4 - len(payload) % 4)
    decoded = base64.urlsafe_b64decode(payload)
    return json.loads(decoded)



class AppState(GoogleAuthState):
    is_authenticating: bool = False
    db_user_id: Optional[int] = None

    stored_email: str = ""
    stored_name: str = ""
    total_secrets: int = 0
    total_shared: int = 0

    origin: str = ""
    share_content: str = ""
    reads: int = 999
    ttl_value: int = 7
    ttl_unit: str = "Days"
    share_url: str = ""
    share_copied: bool = False
    share_error: str = ""

    share_loading: bool = False

    unseal_id: str = ""
    unsealed_content: str = ""
    unseal_reads_left: Optional[int] = None
    unseal_copied: bool = False
    unseal_error: str = ""
    unseal_loading: bool = False

    @rx.var(cache=True)
    def user_name(self) -> str:
        return self.stored_name or ""

    @rx.var(cache=True)
    def user_email(self) -> str:
        return self.stored_email or ""

    @rx.var(cache=True)
    def user_picture(self) -> str:
        return self.tokeninfo.get("picture", "")

    @rx.event
    async def on_login_success(self, response: dict):
        self.is_authenticating = True
        yield
        print(f"DEBUG - on_login_success called, keys: {list(response.keys())}")


        if "credential" in response:
            print("DEBUG - Using credential flow")
            credential = response["credential"]
            token_data = _decode_jwt_payload(credential)
            sub = token_data.get("sub", "")
            email = token_data.get("email", "")
            name = token_data.get("name")
            picture = token_data.get("picture")
            self.token_response_json = json.dumps({"id_token": credential})
            print(f"DEBUG - From credential: sub={sub}, email={email}")
        elif "code" in response:
            print("DEBUG - Using code flow")
            code = response["code"]
            from .config import settings
            redirect_uri = settings.google_redirect_uri
            try:
                async with httpx.AsyncClient() as client:
                    token_response = await client.post(
                        "https://oauth2.googleapis.com/token",
                        data={
                            "code": code,
                            "client_id": settings.google_client_id,
                            "client_secret": settings.google_client_secret,
                            "redirect_uri": redirect_uri,
                            "grant_type": "authorization_code",
                        },
                    )
                    token_response.raise_for_status()
                    token_data = token_response.json()
                    self.token_response_json = json.dumps(token_data)
                    if "refresh_token" in token_data:
                        self.refresh_token = token_data["refresh_token"]
                    id_token = token_data.get("id_token", "")
                    user_data = _decode_jwt_payload(id_token)
                    sub = user_data.get("sub", "")
                    email = user_data.get("email", "")
                    name = user_data.get("name")
                    picture = user_data.get("picture")
                    print(f"DEBUG - From code exchange: sub={sub}, email={email}")
            except Exception as e:
                print(f"DEBUG - Token exchange failed: {e}")
                sub, email, name, picture = "", "", None, ""
        else:
            print("DEBUG - No credential or code in response")
            sub, email, name, picture = "", "", None, ""

        if sub and email:
            # Update local state immediately for a snappy UI
            self.stored_email = email or ""
            self.stored_name = name or ""
            
            # Yield redirect immediately so the user doesn't wait for DB sync
            yield rx.redirect("/home")

            # Perform DB sync in the background
            db = _get_db()
            if db:
                try:
                    user = db.query(User).filter(User.google_sub == sub).first()
                    if not user:
                        user = User(google_sub=sub)
                        db.add(user)
                    
                    user.email = email
                    user.name = name
                    user.picture = picture
                    user.last_login = datetime.utcnow()
                    
                    db.commit()
                    db.refresh(user)
                    self.db_user_id = user.id
                except Exception as e:
                    print(f"Database error during sync: {e}")
                    if db:
                        db.rollback()
                finally:
                    db.close()
        
        self.is_authenticating = False


    @rx.event
    def load_home_data(self):
        sub = self.tokeninfo.get("sub", "")
        if not sub:
            return

        db = _get_db()
        if not db:
            return

        user = db.query(User).filter(User.google_sub == sub).first()
        if user:
            self.db_user_id = user.id
            self.stored_email = user.email or ""
            self.stored_name = user.name or ""
        db.close()

    @rx.event
    def set_share_content(self, value: str):
        self.share_content = value

    @rx.event
    def set_reads(self, value: float):
        try:
            self.reads = int(value)
        except (ValueError, TypeError):
            self.reads = 0

    @rx.event
    def set_ttl_value(self, value: float):
        try:
            self.ttl_value = int(value)
        except (ValueError, TypeError):
            self.ttl_value = 0

    @rx.var(cache=True)
    def line_numbers(self) -> List[str]:
        # Count lines and return list of padded strings like "01", "02", etc.
        lines = self.share_content.count("\n") + 1
        return [str(i).zfill(2) for i in range(1, lines + 1)]

    @rx.var(cache=True)
    def line_numbers_unseal(self) -> List[str]:
        if not self.unsealed_content:
            return ["01"]
        lines = self.unsealed_content.split("\n")
        return [str(i + 1).zfill(2) for i in range(len(lines))]

    @rx.event
    async def handle_file_upload(self, files: List[rx.UploadFile]):
        if not files:
            return
        # Read the first file
        file = files[0]
        content = await file.read()
        try:
            self.share_content = content.decode("utf-8")
        except UnicodeDecodeError:
            self.share_error = "Failed to read file: invalid text encoding."


    @rx.event
    def set_ttl_unit(self, value: str):
        self.ttl_unit = value

    @rx.event
    async def do_share(self):
        self.share_loading = True
        self.share_url = ""
        self.share_error = ""
        yield

        if not self.share_content.strip():
            self.share_error = "Content cannot be empty."
            self.share_loading = False
            return

        try:
            # 1. Encrypt content
            res = encryption.encrypt(self.share_content)
            
            # 2. Prepare TTL and Reads
            ttl_seconds = 0
            try:
                v = float(self.ttl_value)
                if v > 0:
                    multipliers = {"Minutes": 60, "Hours": 3600, "Days": 86400}
                    ttl_seconds = int(v * multipliers.get(self.ttl_unit, 86400))
            except (ValueError, TypeError):
                pass

            reads_left = 0
            try:
                r = int(self.reads)
                if r > 0:
                    reads_left = r
            except (ValueError, TypeError):
                pass


            # 3. Store in Upstash Redis
            redis = redis_client.get_redis_client()
            doc_id = redis_client.store_secret(
                redis, 
                encrypted_data=base64.b64encode(res["encrypted"]).decode(),
                iv_base58=base58.b58encode(res["iv"]).decode(),
                reads=reads_left,
                ttl=ttl_seconds if ttl_seconds > 0 else None
            )

            # 4. Generate composite key (Version 2)
            comp_key = encoding.encode_composite_key(
                version=encoding.LATEST_KEY_VERSION,
                doc_id_base58=doc_id,
                encryption_key=res["key"]
            )

            # Construct full URL using router state
            url_obj = urlparse(self.router.url)
            host = f"{url_obj.scheme}://{url_obj.netloc}"
            self.share_url = f"{host}/unseal#{comp_key}"

            self.share_loading = False

            
        except Exception as e:
            self.share_error = f"Encryption/Storage failed: {str(e)}"
            self.share_loading = False


    @rx.event
    async def copy_share_url(self):
        yield rx.set_clipboard(self.share_url)
        self.share_copied = True
        yield
        await asyncio.sleep(2)
        self.share_copied = False

    @rx.event
    def reset_share(self):
        self.share_content = ""
        self.reads = 999
        self.ttl_value = 7
        self.ttl_unit = "Days"
        self.share_url = ""
        self.share_error = ""

    @rx.event
    def set_unseal_id(self, value: str):
        self.unseal_id = value

    @rx.event
    def do_unseal(self):
        self.unseal_loading = True
        self.unsealed_content = ""
        self.unseal_error = ""
        yield

        comp_key = self.unseal_id.strip()
        if not comp_key:
            self.unseal_error = "Key cannot be empty."
            self.unseal_loading = False
            return

        try:
            # 1. Decode composite key
            decoded = encoding.decode_composite_key(comp_key)
            
            # 2. Fetch from Upstash Redis
            redis = redis_client.get_redis_client()
            record = redis_client.get_secret(redis, decoded["id"])
            
            if not record:
                self.unseal_error = "Document not found or already deleted."
                self.unseal_loading = False
                return

            # 3. Decrypt
            encrypted_bytes = base64.b64decode(record["encrypted"])
            iv_bytes = base58.b58decode(record["iv"])
            
            plaintext = encryption.decrypt(
                encrypted_bytes=encrypted_bytes,
                key=decoded["encryptionKey"],
                iv=iv_bytes,
                version=decoded["version"]
            )
            
            self.unsealed_content = plaintext
            
            # Handle reads left display
            reads = record.get("remainingReads")
            if reads is not None:
                # Since the redis_client decremented it AFTER hgetall, 
                # we show the decremented value.
                self.unseal_reads_left = int(reads) - 1
            else:
                self.unseal_reads_left = None

            self.unseal_loading = False
            
        except Exception as e:
            self.unseal_error = f"Decryption failed: {str(e)}"
            self.unseal_loading = False

    @rx.event
    async def copy_unsealed_content(self):
        yield rx.set_clipboard(self.unsealed_content)
        self.unseal_copied = True
        yield
        await asyncio.sleep(2)
        self.unseal_copied = False

    @rx.event
    def reset_unseal(self):
        self.unseal_id = ""
        self.unsealed_content = ""
        self.unseal_reads_left = None
        self.unseal_copied = False
        self.unseal_error = ""

    @rx.event
    def logout(self):
        self.token_response_json = ""
        self.refresh_token = ""
        return rx.redirect("/")