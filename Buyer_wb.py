import urllib
import json as JSON

import logging
from requests import Session
from exceptions import ServerError


class Buyer_waildberries:
    """
    Для работы с классом необходимо проверять cookies пользователя!
    """

    default_headers = {
        'Connection': 'keep-alive',
        "content-type": "application/json",
        "x-spa-version": "9.1.3",
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
                "value": "37FA68E5534E5B17E068C1DB232582DC09B912692124BC4E622A8951D8BD72C97DB05A3651D644A49733651ACFD2ABF1C883BD131AC6C92550D32DD0587FB6186AFB3D3227F0BD2FF1B4B9CE525F4C6EC3FFB08CC18564A40BED82D9632AD40BB3BEA61DDC7BEFBE3C4B4A3C271D5C62B21CC30B903CC39BE0B50F17B44826A53CE7CB51E9A3CEA74703062CD09D7C8E11957F00F82D7FF02F1349DB5F90CB7A67C35FEAE77BB067C76A7DD52ED15114A8D73F3FFFFED7F9554D9F462388CE6D20C95E5A5602415FFA3A2A34AED5BBAC4A1FF40B21BADF8DBAC34D654C90B3DD0B6BEE5BA25BE54F6A2A58DFB690294451DD0451231F7E3823F3D475D6550477BBBEA23EEFC0A537A4B0B68048DCF65D864A4B14BD2C5367D873E44C9C6D79DA4325B123"
            }
        self.proxy = {
            "https": "http://localhost:8888",
            "http": "http://localhost:8888"
        }

        self.session = Session()
        self.headers = self.default_headers
        self.session.cookies.set(self.cookies["name"], self.cookies["value"])
        self.session.headers.update(self.headers)
        self.session.proxies.update(self.proxy)

    def get_confirm_code(self, number: int) -> bool:
        """
        Авторизация и ввод кода.
        Метод недописан, ещё необходимо проверить:
        5150 - ввод нечитаемых символов с картинки (https://www.wildberries.ru/security/spa/checkcatpcharequirements?forAction=EasyLogin)
        5149. - запрос кода (https://www.wildberries.ru/security/spa/signinprevphone)

        :param number:
        :return:
        """
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

    def handle_errors(self, response: dict) -> bool:
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

    def nm_2_cards(self, id_obj: int):
        """
        Получение ответа сервера по определённому товару.
        Информационная карточка.
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
            url (str): Путь
            json (dict, optional): Данные для выполнения POST. Defaults to None.
            data (str, optional): Данные для выполнения POST. Defaults to None. - используется при смене способа оплаты.

        Kwargs:
            Используются для добавления Params к ссылке

        Raises:
            UnauthorizedError: Ошибка авторизации
            ConnectionError: Ошибка соединения

        Returns:
            dict: Возвращает ответ от сервера
        """
        # При различном теле запроса необходим различный тип.
        if data:
            self.session.headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        elif json:
            self.session.headers['content-type'] = "application/json"
        params = urllib.parse.urlencode(kwargs)  # Формирование строки с параметрами
        if params:
            url += f"?{params}"  # Ссылка для запроса с прараметрами

        # Формирование самого запроса.
        response = self.session.request(
            method=method,
            url=url,
            json=json,
            data=data,
            verify=False
        )
        # Проверка на валидность ответа.
        if response.status_code == 200:
            response_dict = JSON.loads(response.text)
            self.handle_errors(response_dict)
            return response_dict
        else:
            raise ConnectionError

    def add_to_basket(self):
        """
        Метод, который в дальнейшем будет использоваться для закупки определённого количества товара.
        :return:
        """
        pass

    def info_about_cards(self, id_obj: int, ):
        """
        Метод для добавдения товара в карзину через опцию - купить сейчас (количество: 1шт.)
        url - buy_now
        :param id_obj: - id товара, которы мы хотим купить(положить в корзину)
        :return:
        """

        data = self.stock_availability(self.nm_2_cards(id_obj))  # Получение данных о товаре.
        url = "https://www.wildberries.ru/lk/basket/buyitnow/data"

        # "x-spa-version": "9.1.3" - ОЧЕНЬ ВАЖНО ПРОВЕРЯТЬ!

        # Создание запроса для перевода товара в состояние перед покупкой.
        resp = self.handle_request(
            method="POST",
            url=url,
            includeInOrderStr=data["optionId"]  # Берётся из карточки товара.
        )
        for el in resp["value"]["data"]["basket"]["deliveryWays"]:
            if "selectedAddressId" in el:
                # Получение информации о заказе, для оплаты или изменении способа оплаты.
                if el["selectedAddressId"]:
                    data["AddressInfo"]["DeliveryWayCode"] = el["code"]
                    data["AddressInfo"]["selectedAddressId"] = el["selectedAddressId"]
                    if el["code"] == "courier":
                        if len(el["calendars"]) > 0:
                            data["AddressInfo"]["DeliveryPrice"] = el["calendars"][0]["deliveryPrice"]
        open_cards = {}
        for el in resp["value"]["data"]["basket"]["paymentTypes"][0]["bankCards"]:
            # Формирование словаря со всеми доступными картами и необходимой информацией о них.
            if not el["createNew"]:
                open_cards[el["name"]] = {
                    "id": el["id"],
                    "system": el["system"],
                    "select": False
                }
        try:
            # Определение той карты, которая выбрана для оплаты.
            open_cards[resp["value"]["data"]["basket"]["paymentType"]["selectedBankCard"]["name"]]["select"] = True
        except KeyError:
            print("Выбран способ платы не картой!")
        return open_cards, data

    def choosing_a_bank_card(self, name_bank_card: str, open_cards: dict, data: dict) -> bool:
        """
        Выбор карты для оплаты товара.

        Этот метод в дальнейшем можно будет переделать под универсальный способ изменения информации в заказе.
        :param name_bank_card: - номер карты с которой оплачиваем
        :param open_cards: - информация о доступных картах (info_about_cards)
        :param data: - информация о товаре (получаем из info_about_cards, формируется в stock_availability)
        :return:
        """

        # POST https://www.wildberries.ru/spa/yandexaddress/editajax?version=2 # - Ссылка для определения addressId
        # POST https://www.wildberries.ru/spa/deliverypoints - Ссылка на проверку адресов доставки
        # POST https://www.wildberries.ru/spa/removeaddress - Ссылка на изменение адреса
        url = "https://www.wildberries.ru/lk/basket/spa/refresh"

        # Формирование полного набора параметров,которые передаются в теле запроса.
        info = {
            "paymentTypeId": 63,
            "prevPaymentTypeId": 63,
            "includeInOrder[0]": data["optionId"],
            "deliveryWay": data["AddressInfo"]["DeliveryWayCode"],
            "noneIncludedInOrder": False,
            "bankCardId": open_cards[name_bank_card]["id"],
            "addressId": data["AddressInfo"]["selectedAddressId"],
            "isBuyItNowMode": True,
            "unloadCargoOption": ""
        }
        params = urllib.parse.urlencode(info)  # Подготовка параметров.

        # Создание запроса к серверу.
        response = self.handle_request(
            method="POST",
            url=url,
            data=params,
        )

        # Проверка на правильность выполнения запроса. Если карта изменилась на ту, что мы указывали - всё правильно.
        if name_bank_card == response["value"]["basket"]["paymentType"]["selectedBankCard"]["name"]:
            print(f"Выбранная карта: {name_bank_card}")
            for name_card in open_cards.keys():
                open_cards[name_card]['select'] = False
                open_cards[name_bank_card]['select'] = True
            return True
        print("Что-то пошло не так...")
        print(f'Выбранная карта: {response["value"]["basket"]["paymentType"]["selectedBankCard"]["name"]}')
        return False

    def payment_by_card(self, data: dict, cards: dict):
        """
        Запрос оплаты заказа. Ещё нужно тестировать...
        :param cards: - Данные о доступных картах
        :param data: - Данные о товаре
        :return:
        """
        select_card_id = ""
        for card in cards.keys():
            if cards[card]['select'] == True:
                select_card_id = cards[card]['id']
        info = {
            "Delivery": data["AddressInfo"]["DeliveryWayCode"],
            "orderDetails.MaskedCardId": select_card_id,
            "orderDetails.SberPayPhone": "",
            "orderDetails.DeliveryWay": data["AddressInfo"]["DeliveryWayCode"],
            "orderDetails.DeliveryPointId": data["AddressInfo"]["selectedAddressId"],
            "orderDetails.DeliveryPrice": "",  # courier -> int | self -> “”
            "orderDetails.PaymentType.Id": 63,
            "orderDetails.AgreePublicOffert": True,
            "orderDetails.TotalPrice": data["prise"],
            "orderDetails.UserBasketItems.Index": 0,
            "orderDetails.UserBasketItems[0].CharacteristicId": data["optionId"],
            "orderDetails.IncludeInOrder[0]": data["optionId"],
            "orderDetails.UnloadCargoOption": ""
        }
        if data["AddressInfo"]["DeliveryWayCode"] == "self":
            info["address_self"] = data["AddressInfo"]["selectedAddressId"]
        elif data["AddressInfo"]["DeliveryWayCode"] == "courier":
            info["address_courier"] = data["AddressInfo"]["selectedAddressId"]
            info["orderDetails.DeliveryPrice"] = data["AddressInfo"]["DeliveryPrice"]

        url = "https://www.wildberries.ru/lk/basket/spa/submitorder"
        params = urllib.parse.urlencode(info)
        response = self.handle_request(
            method="POST",
            url=url,
            data=params
        )
        try:
            params = response["value"]["url"].split("?")[1]
        except KeyError:
            print(response["value"])
        if self.order_verification(params):
            print("Всё окей")

        else:
            print("Что-то случилось со статусом оплаты заказа...")
        print(f"Заказ: {params}")

    def order_verification(self, params: str) -> bool:
        """
        Метод проверки корректности заказа.

        :param params: принимать из payment_by_card после создания и оплаты заказа.
        :return:
        """
        url = "https://www.wildberries.ru/lk/order/confirmed/data?" + params
        response = self.handle_request(
            method="POST",
            url=url
        )
        if response["value"]["data"]["order"]["orderPaymentStatus"] == "success":
            print("Оплата произошла успешно.")
            return True
        print("Какие-то проблемы с оплатой заказа.")
        return False

    def stock_availability(self, resp: dict) -> dict:
        """
        Требует данных с nm_2_cards
        Обработка полученного ответа от api wildberries и формирование информационной карточки о товаре.

        Достаём лучшую цену, количество на складе, id объекта и формируем заготовку под способ доставки.
        :param resp: - ответ от сервера wildberries
        :return:
        """

        if not resp:
            raise ValueError  # Данные то быть должны
        else:
            try:
                # Основной набор информации.
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
                print(f"Ошибка! \n{ex}")  # В очень ближайшем будущем заменю на нормальное логирование.
            if resp["data"]["products"][0]['sizes'][0]["stocks"]:
                # Определение количества товара на складе
                answ["quantity"] = resp["data"]["products"][0]['sizes'][0]["stocks"][0]["qty"]

            if "salePriceU" in resp["data"]["products"][0]:
                # Определение лучшей цены с условием скидки (Измеряем не в копейках, а в руб.)
                answ["prise"] = min(resp["data"]["products"][0]['priceU'],
                                    resp["data"]["products"][0]['salePriceU']) // 100
            else:
                # Определение цены, если скидки не будет (Измеряем не в копейках, а в руб.)
                answ["prise"] = resp["data"]["products"][0]['salePriceU'] // 100

            print(answ)
            return answ
