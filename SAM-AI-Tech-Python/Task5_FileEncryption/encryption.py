import base64
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_text(text: str, password: str) -> bytes:
    salt = Fernet.generate_key()
    key = derive_key(password, salt)
    cipher = Fernet(key)
    token = cipher.encrypt(text.encode("utf-8"))
    return salt + b":" + token


def decrypt_text(data: bytes, password: str) -> str:
    try:
        salt, token = data.split(b":", 1)
        key = derive_key(password, salt)
        cipher = Fernet(key)
        decrypted = cipher.decrypt(token)
        return decrypted.decode("utf-8")
    except Exception as exc:
        raise ValueError("Invalid password or corrupted file.") from exc


def save_encrypted_file(destination: Path, data: bytes):
    destination.write_bytes(data)


def load_encrypted_file(path: Path) -> bytes:
    return path.read_bytes()
