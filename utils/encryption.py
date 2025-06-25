import base64
import hashlib
from cryptography.fernet import Fernet

def derive_key(master_password) :
    message_digest = hashlib.sha256(master_password.encode().digest())
    return base64.urlsafe_b64encode(message_digest)

def encrypt_service_password(key, password) :
    fernet_key = Fernet(key)
    return fernet_key.encrypt(password.encode()).decode()

def decrypt_service_password(key, token) :
    fernet_key = Fernet(key)
    return fernet_key.decrypt(token.encode()).decode()