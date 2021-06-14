from hashlib import md5
from base64 import b64decode
from base64 import b64encode
# from Crypto.Cipher import AES
# from Crypto.Cipher import AES
from Crypto.Cipher import AES


BLOCK_SIZE = 16  # Bytes
def pad(s): return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s): return s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        base_encoded = b64encode(cipher.encrypt(raw.encode('utf8')))
        decoded = base_encoded.decode("utf-8")
        # for m_pay transaction
        return decoded.replace('+', '-').replace('/', '_').replace('=', ',')

    def decrypt(self, enc):
        enc = enc.replace('-', '+').replace('_', '/').replace(',', '=')
        enc = b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return str(cipher.decrypt(enc), encoding='utf-8').replace('\0', '').replace('<0x00>', '')
