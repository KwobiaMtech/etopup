import requests
import xmltodict as xmltodict
from requests.structures import CaseInsensitiveDict

from api.QueryApis.GloDataClass import GloDataClass
from api.QueryApis.TopUpInterface import TopUpInterface
from config.config import settings


class Glo(TopUpInterface):
    def loadXML(price, msisdn) -> str:
        glo_data = GloDataClass(
            settings.GLO_ACCOUNT_ID,
            settings.GLO_USER,
            settings.GLO_PASSWORD,
            price,
            msisdn
        )
        return glo_data.get_xml()

    @classmethod
    def topup(cls, topup_price, msisdn):
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/xml"
        headers["Accept"] = "application/xml"
        data = cls.loadXML(topup_price, msisdn)
        return cls.queryApi(data, settings.GLO_TOP_UP_API)

    @staticmethod
    def queryApi(data: str, url):
        balance = "not available"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/xml"
        headers["Accept"] = "application/xml"
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
