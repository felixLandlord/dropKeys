import base58

ID_LENGTH = 16
ENCRYPTION_KEY_LENGTH = 16 # 128 bits
LATEST_KEY_VERSION = 2

def encode_composite_key(version: int, doc_id_base58: str, encryption_key: bytes) -> str:
    # doc_id_base58 is the string stored in Redis key
    doc_id_bytes = base58.b58decode(doc_id_base58)
    
    if len(doc_id_bytes) != ID_LENGTH:
        raise ValueError(f"Invalid ID length: expected {ID_LENGTH}, got {len(doc_id_bytes)}")
        
    composite = bytes([version]) + doc_id_bytes + encryption_key
    return base58.b58encode(composite).decode()

def decode_composite_key(composite_key: str):
    decoded = base58.b58decode(composite_key)
    version = decoded[0]
    
    if version not in [1, 2]:
        raise ValueError(f"Unsupported key version: {version}")
        
    doc_id_bytes = decoded[1:1+ID_LENGTH]
    encryption_key = decoded[1+ID_LENGTH:1+ID_LENGTH+ENCRYPTION_KEY_LENGTH]
    
    return {
        "id": base58.b58encode(doc_id_bytes).decode(),
        "encryptionKey": encryption_key,
        "version": version
    }
