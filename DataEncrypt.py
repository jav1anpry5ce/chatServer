import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class DataEncrypt(object):
    def __init__(self):
        self.password = "superSecureDataHere".encode('utf-8')

        self.salt = b'\xcb\\\xb1T\x88#\xa2\xde#\xdc\x01%~\x9e4\xc4'
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        self.key = base64.urlsafe_b64encode(self.kdf.derive(self.password))


    def encryptData(self, data):
        encp = Fernet(self.key)
        data = encp.encrypt(data.encode('utf-8'))
        return data

    def decryptData(self, data):
        decp = Fernet(self.key)
        data = decp.decrypt(data).decode('utf-8')
        return data
