import os
import subprocess
from cryptography.fernet import Fernet
from config.theme import KEY_FILE

def chave_criptografia():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)

        if os.name == "nt":
            subprocess.run(
                ["attrib", "+H", KEY_FILE],
                check=False
            )
    else:
        with open(KEY_FILE, "rb") as file:
            key = file.read()

    return key

cipher_suite = Fernet(chave_criptografia())

def encrypt_password(password: str) -> bytes:
    return cipher_suite.encrypt(password.encode("utf-8"))

def decrypt_password(encrypted_password: bytes) -> str:
    return cipher_suite.decrypt(encrypted_password).decode("utf-8")