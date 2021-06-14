import json
import random
from .AESCipher import AESCipher
from config.config import settings
import requests


class MTN:
    top_up_response: dict = dict()

    def __init__(self, phone, price):
        self.phone = phone
        self.price = price

    @staticmethod
    def get_encrypted_session_data(key):
        param = dict()
        param['RequestUniqueID'] = random.randrange(1111111111, 9999999999)
        param['MethodName'] = 'DstGenerateSessionID'
        json_object = json.dumps(param, indent=0)
        encrypted = AESCipher(key).encrypt(json_object)
        return encrypted

    @staticmethod
    def get_post_data(terminal_id, data):
        return 'TerminalNumber=' + terminal_id + '&Data=' + data

    @staticmethod
    def get_session_id() -> str:
        url = 'http://178.79.179.85:8011/mpay/distribute'
        terminal_id = '17946956'
        key = '1100894491207457'
        data = MTN.get_encrypted_session_data(key)
        response = requests.post(url, MTN.get_post_data(terminal_id, data))
        clean_encrypted = response.json()['Data']
        decrypt = json.loads(AESCipher(key).decrypt(clean_encrypted))
        print('get session id')
        print(decrypt)
        return decrypt['SessionID']

    @staticmethod
    def clean_response_encrypt(text: str) -> str:
        return text.replace('-', '+').replace('_', '/').replace(',', '=')

    @staticmethod
    def get_top_up_data(phone, amount, key):
        param = dict()
        param['SessionID'] = MTN.get_session_id()
        param['RequestUniqueID'] = random.randrange(1111111111, 9999999999)
        param['ProductCode'] = 'MTNFLEXIDB'
        param['SystemServiceID'] = '16'
        param['ReferalNumber'] = phone
        param['Amount'] = str(float(amount * 100))
        param['FromAni'] = ''
        param['Email'] = ''
        param['MethodName'] = 'TopupFlexi'
        json_object = json.dumps(param)
        encrypted_string = AESCipher(key).encrypt(json_object)
        return encrypted_string

    @staticmethod
    def get_topup_post_data(terminal_id, transaction_key, data):
        sending = 'TerminalNumber=' + terminal_id + '&TransactionKey=' + transaction_key + '&Data=' + data
        return sending

    @classmethod
    def top_up(cls, phone, price):
        url = 'http://178.79.179.85:8011/mpay/topup'
        terminal_id = '17946956'
        key = '1100894491207457'
        transaction_key = '1157699898'
        data = cls.get_top_up_data(phone, 0.3, key)
        response = requests.post(url, cls.get_topup_post_data(
            terminal_id, transaction_key, data))
        encrypted_data = response.json()['Data']
        MTN.top_up_response = json.loads(AESCipher(key).decrypt(encrypted_data))
