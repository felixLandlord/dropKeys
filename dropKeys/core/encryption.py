import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt(text: str):
    # AES-GCM 128 (16 byte key)
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    
    # We combine tag + ciphertext to match browser subtle crypto output if needed,
    # or just return them separately. Subtle crypto returns [ciphertext, tag] concatenated.
    return {
        "encrypted": ciphertext + tag,
        "key": key,
        "iv": iv,
    }

def decrypt(encrypted_bytes: bytes, key: bytes, iv: bytes, version: int = 2):
    algorithm = AES.MODE_CBC if version == 1 else AES.MODE_GCM
    
    if algorithm == AES.MODE_GCM:
        # Subtle crypto concatenates tag at the end. Tag is 16 bytes.
        tag = encrypted_bytes[-16:]
        ciphertext = encrypted_bytes[:-16]
        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
    else:
        # AES-CBC (Version 1)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        # Assuming padding was handled or it was a multiple of 16.
        # Browser subtle crypto might have used PKCS7.
        decrypted = cipher.decrypt(encrypted_bytes)
        # Basic unpadding
        pad_len = decrypted[-1]
        return decrypted[:-pad_len].decode()
