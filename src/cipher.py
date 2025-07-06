from abc import ABC, abstractmethod


class Cipher(ABC):
    @abstractmethod
    def encrypt(self, data: str):
        pass

    @abstractmethod
    def decrypt(self, data: str):
        pass
