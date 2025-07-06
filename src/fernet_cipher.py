from src.cipher import Cipher
from setup_logging import logger
from cryptography.fernet import Fernet


class FernetCipher(Cipher):
    def __init__(self, key: bytes, fernet_cipher_logger: logger):
        self.cipher = Fernet(key)
        self._fernet_cipher_logger = logger

    def encrypt(self, data: bytes):
        return self.cipher.encrypt(data)

    def decrypt(self, data: str):
        return self.cipher.decrypt(data)
