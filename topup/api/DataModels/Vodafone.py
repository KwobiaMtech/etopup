import secrets
import xml.etree.ElementTree as ET
import requests
import xmltodict as xmltodict
from requests.structures import CaseInsensitiveDict

from config.config import settings


class Vodafone:
    def get_topup_xml(price, msisdn):
        with open('api/xmlfiles/voda_topup.xml', encoding='latin-1') as f:
            tree = ET.parse(f)
            tree.find('.//cp_id').text = settings.CP_ID
            tree.find('.//cp_transaction_id').text = secrets.token_hex(nbytes=14)
            tree.find('.//user_id').text = msisdn
            tree.find('.//transaction_price').text = str(price)
            tree.write('api/xmlfiles/topup.xml')
            return open('api/xmlfiles/topup.xml', "r").read()

    @staticmethod
    def get_balance_xml():
        with open('api/xmlfiles/voda_get_balance.xml', encoding='latin-1') as f:
            tree = ET.parse(f)
            tree.find('.//cp_id').text = settings.CP_ID
            tree.find('.//cp_transaction_id').text = secrets.token_hex(nbytes=16)
            tree.write('api/xmlfiles/get_balance.xml')
        return open('api/xmlfiles/get_balance.xml', "r").read()

    @staticmethod
    def get_balance():
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/xml"
        headers["Accept"] = "application/xml"
        data = Vodafone.get_balance_xml()
        resp = requests.post(settings.VODAFONE_TOP_UP_API, headers=headers, data=data)
        resp_dict = xmltodict.parse(resp.content)
        return float(resp_dict["cp_reply"]["result"]) / 10000

    @staticmethod
    def topup(topup_price, msisdn):
        price = topup_price * 10000
        url = settings.VODAFONE_TOP_UP_API
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/xml"
        headers["Accept"] = "application/xml"
        data = Vodafone.get_topup_xml(price, msisdn)
        resp = requests.post(url, headers=headers, data=data)
        resp_dict = xmltodict.parse(resp.content)
        return {"status": resp_dict["cp_reply"]["result"], "transaction_id": resp_dict["cp_reply"]["cp_transaction_id"]}
