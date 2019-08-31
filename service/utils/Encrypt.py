from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class Encrypt:
    def __init__(self):
        with open('resources/private_key.pem', 'rb') as file:
            key_content = file.read()
        self.key = RSA.importKey(key_content)

    def encrypt(self, body):
        decryptor = PKCS1_OAEP.new(self.key)
        return decryptor.encrypt(body)

    def decrypt(self, body):
        decryptor = PKCS1_OAEP.new(self.key)
        return decryptor.decrypt(body)

    def decodebase64(self, text):
        return base64.b64decode(text)
