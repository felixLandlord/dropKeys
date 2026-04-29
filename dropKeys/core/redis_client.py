from upstash_redis import Redis
from .encoding import ID_LENGTH
from ..config import settings
import base58
import secrets

def get_redis_client():
    url = settings.upstash_redis_rest_url
    token = settings.upstash_redis_rest_token
    if not url or not token:
        raise ValueError("UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN must be set")
    return Redis(url=url, token=token)

def generate_id() -> str:
    # 16 random bytes as per reference ID_LENGTH
    return base58.b58encode(secrets.token_bytes(ID_LENGTH)).decode()

def store_secret(redis: Redis, encrypted_data: str, iv_base58: str, reads: int, ttl: int = None):
    doc_id = generate_id()
    key = f"dropKeys:{doc_id}"
    
    # Using a dictionary for hset which upstash-redis supports
    data = {
        "encrypted": encrypted_data,
        "iv": iv_base58,
        "remainingReads": reads if reads > 0 else None
    }
    
    # Filter out None values for Redis hset
    data = {k: v for k, v in data.items() if v is not None}
    
    redis.hset(key, values=data)

    
    if ttl and ttl > 0:
        redis.expire(key, ttl)
        
    # Optional: increment global metrics
    redis.incr("dropKeys:metrics:writes")
    
    return doc_id

def get_secret(redis: Redis, doc_id: str):
    key = f"dropKeys:{doc_id}"
    data = redis.hgetall(key)
    
    if not data:
        return None
        
    # Check reads
    remaining = data.get("remainingReads")
    if remaining is not None:
        remaining = int(remaining)
        if remaining <= 1:
            redis.delete(key)
        else:
            redis.hincrby(key, "remainingReads", -1)
            
    return data

