from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from base64 import b64decode

from constant import KEY_FOLDER_PATH


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


def decrypt(message):
    key = RSA.importKey(file_get_contents("resources/private_key.pem"))
    cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
    decrypted_message = cipher.decrypt(b64decode(message))
    return decrypted_message.decode('ASCII', "ignore")


def generate_key():
    new_key = RSA.generate(2048, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    open(KEY_FOLDER_PATH + 'public_key.pem', 'wb').write(public_key)
    open(KEY_FOLDER_PATH + 'private_key.pem', 'wb').write(private_key)


if __name__ == '__main__':
    generate_key()
