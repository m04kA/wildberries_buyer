import urllib
import json as JSON

import requests
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
        'Connection': 'keep-alive',
        "content-type": "application/json",
        "x-spa-version": "9.1.2.1",
        "x-requested-with": "XMLHttpRequest",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.wildberries.ru',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

    def __init__(self, cookies=None, ):
        if cookies:
            self.cookies = {
                "name": "WILDAUTHNEW_V3",
                "value": cookies
            }
        else:
            self.cookies = {
                "name": "WILDAUTHNEW_V3",
                "value": "AD53FF7135AAC8445977A732C61A1F12BB3C00336343C03956D66570FF0135245D5343865CC0B3427DBF09B357076BC915E7BCAF050C23050D70F85D2B42CE01AD74C12E3DF1BBE625CCA88539A9768D944E40F31A076DA1FDC3AFB2FB52AA6C4F3569141DDFB53BF273C0E58D555F2FD2AF2581FAA8239F2F6B96122222A535005ECB5FC96C65F689B223C2DEC178C24009826DCF2A5C21F9B94F429DC25BC0ACBD65470B2AFB0072CEB8D85952A2237F5E78198042C59BAECD81E59723013E618776A201A228B95397B85FA9167FA1F623D6D47A1E6AA59809FB1756645C3F0ABCDF3C064299A46AD92738813ACFBAC4E3AC72A9563363800A11F3621EEEA35B40EC52EDFAF2EA6668827D96A01BAE35B2AB3C3A075BA7679989BFFFA88F6A3FFC767C"
            }
        self.proxy = {
            "https": "http://localhost:8888",
            "http": "http://localhost:8888"
        }

        self.session = Session()
        self.headers = self.default_headers
        self.session.cookies.set(self.cookies["name"], self.cookies["value"])
        self.session.headers.update(self.headers)
        # self.session.proxies.update(self.proxy)

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
                       data: str = None,
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
        if data:
            self.session.headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        elif json:
            self.session.headers['content-type'] = "application/json"
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
            data=data
        )
        if response.status_code == 200:
            response_dict = JSON.loads(response.text)
            handle_errors(response_dict)
            return response_dict
        else:
            return response

    def add_to_basket(self):
        pass

    def info_about_cards(self, id_obj: int, ):
        """
        url - buy_now
        :param id_obj: - id товара, которы мы хотим купить(положить в корзину)
        :return:
        """

        data = self.stock_availability(self.nm_2_cards(id_obj))
        url = "https://www.wildberries.ru/lk/basket/buyitnow/data"

        resp = self.handle_request(
            method="POST",
            url=url,
            includeInOrderStr=data["optionId"]
        )
        open_cards = {}
        for el in resp["value"]["data"]["basket"]["paymentTypes"][0]["bankCards"]:
            if not el["createNew"]:
                open_cards[el["name"]] = {
                    "id": el["id"],
                    "system": el["system"],
                    "select": False
                }
        try:
            open_cards[resp["value"]["data"]["basket"]["paymentType"]["selectedBankCard"]["name"]]["select"] = True
        except KeyError:
            print("Выбран способ платы не картой!")
        return open_cards, data

    def choosing_a_bank_card(self, name_bank_card: str, open_cards: dict, data: dict) -> bool:
        """
        Выбор карты для оплаты товара.
        :param name_bank_card: - номер карты с которой оплачиваем
        :param open_cards: - информация о доступных картах (info_about_cards)
        :param data: - информация о товаре (получаем из info_about_cards, формируется в stock_availability)
        :return:
        """
        url = "https://www.wildberries.ru/lk/basket/spa/refresh"
        self.session.headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        data = f"paymentTypeId=63&prevPaymentTypeId=63&includeInOrder%5B0%5D={data['optionId']}&deliveryWay=self&noneIncludedInOrder=false&bankCardId=35a15a2e-3cd4-11ec-bfef-96737a2a6dae&addressId=111104&isBuyItNowMode=true&unloadCargoOption="
        response = self.handle_request(
            method="POST",
            url=url,
            data=data,
        )
        if name_bank_card is response["value"]["basket"]["paymentType"]["selectedBankCard"]["name"]:
            print(f"Выбранная карта: {name_bank_card}")
            return True
        print(f'Выбранная карта: {response["value"]["data"]["basket"]["paymentType"]["selectedBankCard"]["name"]}')
        return False

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
            try:
                answ = {
                    "name": resp["data"]["products"][0]["name"],
                    "id_obj": resp["data"]["products"][0]['id'],
                    "quantity": 0,
                    "prise": min(resp["data"]["products"][0]['priceU'],
                                 resp["data"]["products"][0]['salePriceU']) // 100,
                    "optionId": resp["data"]["products"][0]['sizes'][0]["optionId"]
                }
            except Exception as ex:
                print(f"Ошибка! \n{ex}")
            if resp["data"]["products"][0]['sizes'][0]["stocks"]:
                answ["quantity"] = resp["data"]["products"][0]['sizes'][0]["stocks"][0]["qty"]

            if "salePriceU" in resp["data"]["products"][0]:
                answ["prise"] = min(resp["data"]["products"][0]['priceU'],
                                    resp["data"]["products"][0]['salePriceU']) // 100
            else:
                answ["prise"] = resp["data"]["products"][0]['salePriceU'] // 100

            print(answ)
            return answ
