import hashlib

def generate_signature(raw_value_str: str, key: str, iterations: int) -> str:
    """
    Generates a PBKDF2 HMAC SHA256 signature.
    Secret key = password
    Raw value = salt
    """
    password_bytes = key.encode('utf-8')
    salt_bytes = raw_value_str.encode('utf-8')

    hash_bytes = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password_bytes,
        salt=salt_bytes,
        iterations=iterations
    )

    return hash_bytes.hex()
