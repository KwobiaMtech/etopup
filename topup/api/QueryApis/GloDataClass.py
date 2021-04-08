import secrets
from dataclasses import dataclass
import xml.etree.ElementTree as ET

import requests
import xmltodict
from requests.structures import CaseInsensitiveDict

from config.config import settings


@dataclass
class GloDataClass:
    account_id: str
    user: str
    password: str
    price: str
    msisdn: str
    path: str = "api/xmlfiles/glo_etopup.xml"

    def get_xml(self):
        with open(self.path, encoding='latin-1') as f:
            tree = ET.parse(f)
            tree.find('.//clientId').text = self.account_id
            tree.find('.//clientReference').text = secrets.token_hex(nbytes=14)
            tree.find('.//initiatorPrincipalId/id').text = self.account_id
            tree.find('.//initiatorPrincipalId/userId').text = self.user
            tree.find('.//password').text = self.password
            tree.find('.//senderPrincipalId/id').text = self.account_id
            tree.find('.//senderPrincipalId/userId').text = self.user
            tree.find('.//topupPrincipalId/id').text = self.msisdn
            tree.find('.//senderAccountSpecifier/accountId').text = self.account_id
            tree.find('.//topupAccountSpecifier/accountId').text = self.msisdn
            tree.find('.//amount/value').text = str(self.price)
            tree.write('api/xmlfiles/glotopup.xml')
            return open('api/xmlfiles/glotopup.xml', "r").read()
