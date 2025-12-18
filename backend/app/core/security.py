from cryptography.fernet import Fernet
from app.core.config import settings

# Ensure FERNET_KEY is set in config/env
# settings.FERNET_KEY should be a 32 url-safe base64-encoded bytes
# For now, we'll generate one if missing for dev, but in prod this must be env var
try:
    _cipher_suite = Fernet(settings.FERNET_KEY)
except Exception:
    # Fallback for dev only - DO NOT USE IN PROD without env var
    # This keeps existing code running if they didn't set the key yet
    key = Fernet.generate_key()
    _cipher_suite = Fernet(key)

def encrypt_string(plain_text: str) -> str:
    if not plain_text:
        return ""
    encrypted_bytes = _cipher_suite.encrypt(plain_text.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_string(encrypted_text: str) -> str:
    if not encrypted_text:
        return ""
    decrypted_bytes = _cipher_suite.decrypt(encrypted_text.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')
