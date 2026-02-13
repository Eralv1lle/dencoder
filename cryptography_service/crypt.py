from cryptography.fernet import Fernet
from .get_key import get_key


def encrypt(text: str, data_id: int):
    key = get_key(data_id)
    cipher = Fernet(key)
    return cipher.encrypt(text.encode())

def decrypt(encrypted: str, data_id: int):
    key = get_key(data_id)
    cipher = Fernet(key)
    return cipher.decrypt(encrypted).decode()



