import urllib
import json as JSON

import requests
from requests import Session
from exceptions import ServerError


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
    """
    Для работы с классом необходимо проверять cookies пользователя!
    """

    default_headers = {
        'Connection': 'keep-alive',
        "content-type": "application/json",
        "x-spa-version": "9.1.2.2",
        "x-requested-with": "XMLHttpRequest",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
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
                "value": "79D0FB26A56005AD0CE889397F5E6B964563FE3FE861C9DD9D9AC237EDA1D2D69071D25D7597CAC4D76C95E22B7CFE229C4079FF675C4355324E5DC1CDBEC2A537D0639D0C3B04420EA049728A6A258838122C1D8CB0861B6B13E4F203E8D9C7EA289A3AD43C44AC9258919F5DD5705488F89FD04BEFCC7976D24862FBA1FA985EB88199EBDF2EB22F1E2D6F653AFCE1C9DE637D1FAA3E9E5B3E0B8CD544088A579CE50C02BA63E976BB0DF0A71DC1AE6860317738407D2F7D99987D92071E51F2F26F681C3F8A2AFA6B426D63DCE6CA0F8605CF1429DED8E8C756644E08F41A106C2B1BB468376C071BC35D889932559A8DEBECFD6CF57B36BB04C719D10F9F754E37594433409B51AB1B5613AE0B498730E5B30A53188F651BDF6F390A76E99403B356"
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
        params = urllib.parse.urlencode(kwargs)
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
            raise ConnectionError

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
        for el in resp["value"]["data"]["basket"]["deliveryWays"]:
            if "selectedAddressId" in el:
                if el["selectedAddressId"]:
                    data["AddressInfo"]["DeliveryWayCode"] = el["code"]
                    data["AddressInfo"]["selectedAddressId"] = el["selectedAddressId"]
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

        # POST https://www.wildberries.ru/spa/yandexaddress/editajax?version=2 # - Ссылка для определения addressId

        url = "https://www.wildberries.ru/lk/basket/spa/refresh"
        info = {
            "paymentTypeId": 63,
            "prevPaymentTypeId": 63,
            "includeInOrder[0]": data["optionId"],
            "deliveryWay": data["AddressInfo"]["DeliveryWayCode"],
            "noneIncludedInOrder": False,
            "bankCardId": open_cards[name_bank_card]["id"],
            "addressId": data["AddressInfo"]["selectedAddressId"],  # Меняется при смене пользователя
            "isBuyItNowMode": True,
            "unloadCargoOption": ""
        }
        params = urllib.parse.urlencode(info)
        response = self.handle_request(
            method="POST",
            url=url,
            data=params,
        )
        if name_bank_card is response["value"]["basket"]["paymentType"]["selectedBankCard"]["name"]:
            print(f"Выбранная карта: {name_bank_card}")
            return True
        print(f'Выбранная карта: {response["value"]["data"]["basket"]["paymentType"]["selectedBankCard"]["name"]}')
        return False

    def payment_by_card(self, data):
        url = "https://www.wildberries.ru/lk/basket/spa/submitorder"
        response = self.handle_request(
            method="POST",
            url=url
        )

    def stock_availability(self, resp: dict) -> dict:
        """
        Требует данных с nm_2_cards
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
                    "optionId": resp["data"]["products"][0]['sizes'][0]["optionId"],
                    "AddressInfo": {}
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
