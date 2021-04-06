import secrets
import xml.etree.ElementTree as ET
import requests
import xmltodict as xmltodict
from requests.structures import CaseInsensitiveDict
from config.config import settings


class Glo:
    def get_topup_xml(price, msisdn):
        with open('api/xmlfiles/glo_etopup.xml', encoding='latin-1') as f:
            account_id = settings.GLO_ACCOUNT_ID
            user = settings.GLO_USER
            password = settings.GLO_PASSWORD
            tree = ET.parse(f)
            tree.find('.//clientId').text = account_id
            tree.find('.//clientReference').text = secrets.token_hex(nbytes=14)
            tree.find('.//initiatorPrincipalId/id').text = account_id
            tree.find('.//initiatorPrincipalId/userId').text = user
            tree.find('.//password').text = password
            tree.find('.//senderPrincipalId/id').text = account_id
            tree.find('.//senderPrincipalId/userId').text = user
            tree.find('.//topupPrincipalId/id').text = msisdn
            tree.find('.//senderAccountSpecifier/accountId').text = account_id
            tree.find('.//topupAccountSpecifier/accountId').text = msisdn
            tree.find('.//amount/value').text = str(price)
            tree.write('api/xmlfiles/glotopup.xml')
            return open('api/xmlfiles/glotopup.xml', "r").read()

    @staticmethod
    def get_balance_xml():
        with open('api/xmlfiles/voda_get_balance.xml', encoding='latin-1') as f:
            tree = ET.parse(f)
            tree.find('.//cp_id').text = 'kenee3'
            tree.find('.//cp_transaction_id').text = secrets.token_hex(nbytes=16)
            tree.write('api/xmlfiles/get_balance.xml')
        return open('api/xmlfiles/get_balance.xml', "r").read()

    @staticmethod
    def topup(topup_price, msisdn):
        balance = "not_available"
        url = settings.GLO_TOP_UP_API
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/xml"
        headers["Accept"] = "application/xml"
        data = Glo.get_topup_xml(topup_price, msisdn)
        resp = requests.post(url, headers=headers, data=data)
        resp_dict = xmltodict.parse(resp.content)
        status = resp_dict["soap:Envelope"]["soap:Body"]["ns2:requestTopupResponse"]["return"]["resultCode"]
        reference = resp_dict["soap:Envelope"]["soap:Body"]["ns2:requestTopupResponse"]["return"]["ersReference"]
        if status == "0":
            balance = resp_dict["soap:Envelope"]["soap:Body"]["ns2:requestTopupResponse"]["return"]["senderPrincipal"][
                "accounts"]["account"]["balance"]["value"]
        description = resp_dict["soap:Envelope"]["soap:Body"]["ns2:requestTopupResponse"]["return"]["resultDescription"]
        return {
            "status": status,
            "reference": reference,
            "description": description,
            "balance": balance,
        }
