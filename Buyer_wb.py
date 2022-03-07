import urllib
import json as JSON

from requests import Session
from exceptions import ServerError

# По товару


id_obj = 16023989
url_obj = f"https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?&&stores=117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043&pricemarginCoeff=1.0&reg=1&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,3,18,15,21&dest=-1029256,-102269,-1252558,-445282&nm={id_obj}"


def handle_errors(response: dict) -> bool:
    """Обработка ошибок

    Args:
        response (dict): Ответ от сервера

    Raises:
        ServerError: Ошибка сервера

    Returns:
        bool: Возвращает True при отсутствии ошибок
    """
    if 'error' in response:
        raise ServerError(response['error'])
    return True


class Buyer_waildberries:
    default_headers = {
        'Host': 'wbxcatalog-ru.wildberries.ru',
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.wildberries.ru',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.wildberries.ru/catalog/60181354/detail.aspx?targetUrl=MI',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

    def __init__(self,cookies=None,):
        if cookies:
            self.cookies = {
                "WILDAUTHNEW_V3": cookies
            }
        else:
            self.cookies = {
                "WILDAUTHNEW_V3": "8DCF18261BA034889B058109D6C0C8AFB83C9C53F64D32F5A73274EAE1AF1757FB1C66D0FE8B3E10D834B0C1883DB996A024800F7A6EB5FF78542C0CBBBA5DEC94756AEA617928959E338B54C8E93F20D222C22D17DFA2A5F4CBA5F085BC93CCF6D587A0FE8573DB086EE252E9F1F8698B2924AB471DB8964380615213B5EEED0DAE8F54548FB2DA0BFDB69B9530E8DC93B06B2ABFAE54A152E89DFD04E9A77D9AA19E5F4965A7205859CACD840AC3CBB53B75135BF2FAD976B84FB1C24120040A5061730FD596A788125963508C6F6766CF73F237E6C95FE74E0ABD1FCFE4DCD13179E1D1AC5AB83EF09ED1464518E68A508F3B9ABD6C2B022A2D791F374A9A16CCE230D1244CD28C9773480C7BAC93FB50A7E5B0DC0E7FB92E569C574AE77C8BE21A8E"
            }

        self.session = Session()
        self.headers = self.default_headers

    def get_confirm_code(self, number: int) -> bool:
        """
        Авторизация и ввод кода.
        Метод недописан, ещё необходимо проверить:
        5150 - ввод нечитаемых символов с картинки (https://www.wildberries.ru/security/spa/checkcatpcharequirements?forAction=EasyLogin)
        5149. - запрос кода (https://www.wildberries.ru/security/spa/signinprevphone)

        :param number:
        :return:
        """
        # 5151 - num req
        # phone - 79127477972
        url = "https://www.wildberries.ru/mobile/requestconfirmcode?forAction=EasyLogin"
        json = {
            "phoneInput.AgreeToReceiveSmsSpam": False,
            "phoneInput.ConfirmCode": None,  # ?
            "phoneInput.FullPhoneMobile": number,
            "returnUrl": "https % 3A % 2F % 2Fwww.wildberries.ru % 2F",
            "phonemobile": number,
            "agreeToReceiveSms": False,
            "shortSession": False,
            "period": "ru",
            "prevPhoneAuth": number
        }
        resp = self.handle_request(
            method="POST",
            url="https://www.wildberries.ru/mobile/requestconfirmcode",
            json=json,
            forAction="EasyLogin"
        )

    def init_auth(self) -> bool:
        # 445
        url = "https://www.wildberries.ru/security/spa/signinsignup"

    def nm_2_cards(self, id_obj: int):
        """
        Получение ответа сервера по определённому товару.
        :param id_obj: - id товара.
        :return:
        """
        return self.handle_request(method="GET",
                                   url="https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog",
                                   json=None,
                                   spp=19,
                                   regions="64,86,83,75,4,38,30,33,70,71,22,31,66,68,1,82,48,40,69,80",
                                   stores="117673,122258,122259,125238,125239,125240,6159,507,3158,117501,120602,120762,6158,121709,124731,159402,2737,130744,117986,1733,686,132043",
                                   pricemarginCoeff=1.0,
                                   reg=1,
                                   appType=1,
                                   offlineBonus=0,
                                   onlineBonus=0,
                                   emp=0,
                                   locale="ru",
                                   lang="ru",
                                   curr="rub",
                                   couponsGeo="12,3,18,15,21",
                                   dest="-1029256,-102269,-1252558,-445282",
                                   nm=id_obj)

    def handle_request(self,
                       method: str,
                       url: str,
                       json: dict = None,
                       **kwargs) -> dict:
        """Запрос к серверу

        Args:
            method (str): Метод
            path (str): Путь
            json (dict, optional): Данные для выполнения POST. Defaults to None.

        Kwargs:
            Используются для добавления Params к ссылке

        Raises:
            UnauthorizedError: Ошибка авторизации
            ConnectionError: Ошибка соединения

        Returns:
            dict: Возвращает ответ от сервера
        """
        params = '&'.join([
            str(x) + "=" + urllib.parse.quote_plus(str(y))
            for x, y in kwargs.items()
        ])
        if params:
            url += f"?{params}"

        response = self.session.request(
            method=method,
            url=url,
            json=json,
            headers=self.headers,
            cookies=self.cookies,
        )
        if isinstance(response, object):
            response_dict = JSON.loads(response.text)
            handle_errors(response_dict)
            return response_dict
        else:
            raise ConnectionError

    def buy_moment(self, id_obj: int, ):
        data = self.stock_availability(self.nm_2_cards(id_obj))
        url = "https://www.wildberries.ru/lk/basket/buyitnow/data"
        resp = self.handle_request(
            method="POST",
            url=url,
            json=None,
            includeInOrderStr=data["optionId"]
        )
        open_cards = []
        for el in resp["value"]["data"]["basket"]["paymentTypes"][0]["bankCards"]:
            if not el["createNew"]:
                open_cards.append({
                    "name": el["name"],
                    "system": el["system"]
                })
        return open_cards



    def stock_availability(self, resp: dict) -> dict:
        """
        Обработка полученного ответа от api wildberries.

        Если есть товар, то достаём от туда цену и количество на складе.
        :param resp: - ответ от сервера wildberries
        :return:
        """

        if not resp:
            raise ValueError
        else:
            if resp["data"]["products"][0]['sizes'][0]["stocks"]:
                if "salePriceU" in resp["data"]["products"][0]:
                    answ = {
                        "id_obj": resp["data"]["products"][0]['id'],
                        "quantity": resp["data"]["products"][0]['sizes'][0]["stocks"][0]["qty"],
                        "prise": min(resp["data"]["products"][0]['priceU'],
                                     resp["data"]["products"][0]['salePriceU']) // 100,
                        "optionId": resp["data"]["products"][0]['sizes'][0]["optionId"]
                    }
                else:
                    answ = {
                        "id_obj": resp["data"]["products"][0]['id'],
                        "quantity": resp["data"]["products"][0]['sizes'][0]["stocks"][0]["qty"],
                        "prise": resp["data"]["products"][0]['priceU'] // 100,
                        "optionId": resp["data"]["products"][0]['sizes'][0]["optionId"]
                    }
            else:
                if "salePriceU" in resp["data"]["products"][0]:
                    answ = {
                        "id_obj": resp["data"]["products"][0]['id'],
                        "quantity": 0,
                        "prise": min(resp["data"]["products"][0]['priceU'],
                                     resp["data"]["products"][0]['salePriceU']) // 100
                    }
                else:
                    answ = {
                        "id_obj": resp["data"]["products"][0]['id'],
                        "quantity": 0,
                        "prise": resp["data"]["products"][0]['priceU'] // 100
                    }
            return answ
