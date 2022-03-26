import urllib
import json as JSON
from pprint import pprint
from requests import Session
from exceptions import ServerError
from SingIn import get_cookie_user
from loguru import logger


class Buyer_waildberries:
    """
    Для работы с классом необходимо проверять cookies пользователя!
    """

    default_headers = {
        'Connection': 'keep-alive',
        "content-type": "application/json",
        "x-spa-version": "9.1.3.20",
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
            my_cookie = get_cookie_user()
            self.cookies = {
                "name": "WILDAUTHNEW_V3",
                "value": my_cookie
            }
        self.proxies = {
            "https": "http://localhost:8888",
            "http": "http://localhost:8888"
        }

        self.session = Session()
        self.data = {}
        logger.debug(f"Start session - {self.session}")
        self.headers = self.default_headers
        self.session.cookies.set(self.cookies["name"], self.cookies["value"])
        logger.debug(f"Set cookies - {self.cookies}")
        self.session.headers.update(self.headers)
        logger.debug(f"Set headers - {self.headers}")
        self.session.proxies.update(self.proxies)
        logger.debug(f"Set proxies - {self.proxies}")

    def get_confirm_code(self, number: int):
        """
        Авторизация и ввод кода.
        Метод недописан, ещё необходимо проверить:
        ввод нечитаемых символов с картинки (https://www.wildberries.ru/security/spa/checkcatpcharequirements?forAction=EasyLogin)
        запрос кода (https://www.wildberries.ru/security/spa/signinprevphone)

        :param number:
        :return:
        """
        url = "https://www.wildberries.ru/mobile/requestconfirmcode?forAction=EasyLogin"
        json = {
            "phoneInput.AgreeToReceiveSmsSpam": False,
            "phoneInput.ConfirmCode": None,  # ?
            "phoneInput.FullPhoneMobile": number,
            "returnUrl": "https://www.wildberries.ru/",
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

    @logger.catch()
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
        if json:
            self.session.headers['content-type'] = "application/json"
            logger.debug(f"Set content-type:\napplication/json")
        else:
            self.session.headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            logger.debug(f"Set content-type:\napplication/x-www-form-urlencoded; charset=UTF-8")

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
        logger.debug(f"Do request to server:\n"
                     f"method - {method}\n"
                     f"url - {url}\n"
                     f"json - {json}\n"
                     f"data - {data}")
        # Проверка на валидность ответа.
        if response.status_code == 200:
            response_dict = JSON.loads(response.text)
            self.handle_errors(response_dict)
            logger.info(f'Successful - {url}')
            return response_dict
        else:
            logger.error(ConnectionError)
            raise ConnectionError

    def add_to_basket(self, quantity: int) -> bool:
        """
        Метод, который в дальнейшем будет использоваться для закупки определённого количества товара.
        :return:
        """
        self.del_all_obj_in_basket()
        url = "https://www.wildberries.ru/product/addtobasket"
        # Формируем тело запроса
        info = {
            "cod1S": self.data["id_obj"],
            "characteristicId": self.data["optionId"],
            "quantity": quantity
        }
        params = urllib.parse.urlencode(info)
        logger.info(f"Add to basket object (id - {self.data['id_obj']}; quantity - {quantity})")
        response = self.handle_request(
            method="POST",
            url=url,
            data=params
        )
        # Проверка на соответствие в корзине.
        if response["value"]["basketInfo"]["basketQuantity"] == quantity:
            logger.info(f"Successful add to basket object (id - {self.data['id_obj']}; quantity - {quantity})")
            return True
        return False

    def get_info_from_basket(self) -> list:
        """
        Достаём id всех заказов для отчистки корзины.
        :return:
        """
        logger.info(f"Get info from basket.")
        url = "https://www.wildberries.ru/lk/basket/data"
        response = self.handle_request(
            method="POST",
            url=url
        )
        answ = []
        empty = {
            "resultState": 0
        }
        if response == empty:
            return answ
        items = response["value"]["data"]["basket"]["basketItemsByDeliveryDate"][0]["items"]
        for el in items:
            answ.append(el['id'])
        logger.info(f"Successful get info from basket.")
        return answ

    def del_all_obj_in_basket(self):
        """
        Функция по полной отчистке корзины
        :return:
        """
        optionIds = self.get_info_from_basket()
        logger.info(f"Delete {optionIds} from basket")
        url = "https://www.wildberries.ru/lk/basket/spa/delete"
        for id in optionIds:
            info = {"chrtIds[0]": id}
            params = urllib.parse.urlencode(info)
            response = self.handle_request(
                method="POST",
                url=url,
                data=params
            )

        logger.info(f"Successful delete {optionIds} from basket")

    def get_delivery_info(self, data: dict) -> dict:
        """
        Получаем информацию о доставке из запроса по добавлению товара в корзину.
        :param data: - response
        :return:
        """
        answer = {"AddressInfo": {}}
        for el in data:
            if "selectedAddressId" in el:
                # Получение информации о заказе, для оплаты или изменении способа оплаты.
                if el["selectedAddressId"]:
                    answer["AddressInfo"]["DeliveryWayCode"] = el["code"]
                    answer["AddressInfo"]["selectedAddressId"] = el["selectedAddressId"]
                    if el["code"] == "courier":
                        if len(el["calendars"]) > 0:
                            answer["AddressInfo"]["DeliveryPrice"] = el["calendars"][0]["deliveryPrice"]
        return answer

    def info_about_cards(self, id_obj: int, ) -> dict:
        """
        Метод для добавдения товара в карзину через опцию - купить сейчас (количество: 1шт.)
        url - buy_now
        :param id_obj: - id товара, которы мы хотим купить(положить в корзину)
        :return:
        """

        logger.debug(f"Get info about - {id_obj}")
        self.data = self.stock_availability(self.nm_2_cards(id_obj))  # Получение данных о товаре.
        logger.debug(f"Successful request about - {id_obj}")

        if not self.add_to_basket(1):
            raise ValueError("Wrong add to basket. (some obj there is...)")
        else:
            print(f'Товар успешно добавлен в корзину (id - {self.data["id_obj"]})')

        url = "https://www.wildberries.ru/lk/basket/buyitnow/data"
        # Создание запроса для перевода товара в состояние перед покупкой.
        help_url = urllib.parse.urlencode({"includeInOrderStr": self.data["optionId"]})
        self.session.headers.update({"Referer": url + help_url})
        logger.debug(f"Move {id_obj} create order.")
        resp = self.handle_request(
            method="POST",
            url=url,
            includeInOrderStr=self.data["optionId"]  # Берётся из карточки товара.
        )
        self.session.headers.update({"Referer": None})
        logger.debug(f"Successful request basket_order - {id_obj}")
        try:
            data_help = resp["value"]["data"]["basket"]
        except KeyError:
            # "x-spa-version": "9.1.3.12" - ОЧЕНЬ ВАЖНО ПРОВЕРЯТЬ!
            logger.error(f"Wrong headers! (id - {self.data['id_obj']})")
            raise KeyError("Wrong headers!")
        # Обнавляем данные о товре - добавление доставки
        self.data = self.data | self.get_delivery_info(data_help["deliveryWays"])

        try:
            bank_cards = data_help["paymentTypes"][0]["bankCards"]
        except KeyError as ex:
            error = data_help["paymentTypes"][0]["errorTip"]
            logger.error(f'Delivery is not define. (id obj - {self.data["id_obj"]})')
            raise KeyError(error)
        open_cards = self.create_dict_open_card(bank_cards)
        try:
            # Определение той карты, которая выбрана для оплаты.
            card = resp["value"]["data"]["basket"]["paymentType"]["selectedBankCard"]["name"]
            open_cards[card]["select"] = True
            logger.info(f"Define selected bank card - {card}")
        except KeyError:
            logger.error(f"Incorrect payment option")
            print("Выбран способ платы не картой!")
        return open_cards

    def create_dict_open_card(self, data: list) -> dict:
        """
        Создание списка доступных банковских карт на аккаунте.
        :param data:
        :return:
        """
        answ = {}
        for el in data:
            if not el["createNew"]:
                answ[el["name"]] = {
                    "id": el["id"],
                    "system": el["system"],
                    "select": False
                }
        return answ

    def choosing_a_bank_card(self, name_bank_card: str, open_cards: dict) -> bool:
        """
        Выбор карты для оплаты товара.

        Этот метод в дальнейшем можно будет переделать под универсальный способ изменения информации в заказе.
        :param name_bank_card: - номер карты с которой оплачиваем
        :param open_cards: - информация о доступных картах (info_about_cards)
        :param data: - информация о товаре (получаем из info_about_cards, формируется в stock_availability)
        :return:
        """

        logger.info(f"Refresh choosing bank card to {name_bank_card}.")
        # POST https://www.wildberries.ru/spa/yandexaddress/editajax?version=2 # - Ссылка для определения addressId
        # POST https://www.wildberries.ru/spa/deliverypoints - Ссылка на проверку адресов доставки
        # POST https://www.wildberries.ru/spa/removeaddress - Ссылка на изменение адреса
        url = "https://www.wildberries.ru/lk/basket/spa/refresh"

        # Формирование полного набора параметров,которые передаются в теле запроса.
        info = {
            "paymentTypeId": 63,
            "prevPaymentTypeId": 63,
            "includeInOrder[0]": self.data["optionId"],
            "deliveryWay": self.data["AddressInfo"]["DeliveryWayCode"],
            "noneIncludedInOrder": False,
            "bankCardId": open_cards[name_bank_card]["id"],
            "addressId": self.data["AddressInfo"]["selectedAddressId"],
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
        flag = self.check_right_card(
            name_bank_card,
            response["value"]["basket"]["paymentType"]["selectedBankCard"]["name"]
        )
        if flag:
            open_cards = self.update_select_card(open_cards, name_bank_card)
        return flag

        # if name_bank_card == response["value"]["basket"]["paymentType"]["selectedBankCard"]["name"]:
        #     print(f"Выбранная карта: {name_bank_card}")
        #     logger.info(f'Select bank card - {name_bank_card}')
        #     for name_card in open_cards.keys():
        #         open_cards[name_card]['select'] = False
        #     open_cards[name_bank_card]['select'] = True
        #     logger.info(f"Successful change bank card to {name_card}")
        #     return True
        # actual_card = response["value"]["basket"]["paymentType"]["selectedBankCard"]["name"]
        # logger.error(f"Fail to change the card. Now select card - {actual_card}")
        # print("Что-то пошло не так...")
        # print(f'Выбранная карта: {actual_card}')
        # return False

    def check_right_card(self, number: str, response_number: str) -> bool:
        """
        Проверка на успех замены карты
        :param number: - Номер нашей выбранной карты
        :param response_number: - Номер карты из ответа сервера.
        :return: - True, если всё совпадает иначе False
        """
        if number == response_number:
            print(f"Выбранная карта: {number}")
            logger.info(f'Select bank card - {number}')
            return True
        logger.error(f"Fail to change the card. Now select card - {response_number}")
        print("Что-то пошло не так...")
        print(f'Выбранная карта: {response_number}')
        return False

    def update_select_card(self, open_cards: dict, select_card: str) -> dict:
        """
        Обновление динамических данных о доступных карточек для оплаты.
        :param open_cards: - Старый набор данных о доступных картах
        :param select_card: - Номер выбранной карты, с которой будет оплата.
        :return:
        """
        for name_card in open_cards.keys():
            open_cards[name_card]['select'] = False
        open_cards[select_card]['select'] = True
        logger.info(f"Successful change bank card to {name_card}")
        return open_cards

    def payment_by_card(self, cards: dict):
        """
        Запрос оплаты заказа.
        Необходимо сделать ввод кода с мобильного банка.
        :param cards: - Данные о доступных картах
        :param data: - Данные о товаре
        :return:
        """

        select_card_id = ""
        for card in cards.keys():
            if cards[card]['select']:
                select_card_id = cards[card]['id']
                logger.info(f"Order payment start:\n"
                            f"id object - {self.data['id_obj']}\n"
                            f"select card - {card}")
        info = {
            "Delivery": self.data["AddressInfo"]["DeliveryWayCode"],
            "orderDetails.MaskedCardId": select_card_id,
            "orderDetails.SberPayPhone": "",
            "orderDetails.DeliveryWay": self.data["AddressInfo"]["DeliveryWayCode"],
            "orderDetails.DeliveryPointId": self.data["AddressInfo"]["selectedAddressId"],
            "orderDetails.DeliveryPrice": "",  # courier -> int | self -> “”
            "orderDetails.PaymentType.Id": 63,
            "orderDetails.AgreePublicOffert": True,
            "orderDetails.TotalPrice": self.data["prise"],
            "orderDetails.UserBasketItems.Index": 0,
            "orderDetails.UserBasketItems[0].CharacteristicId": self.data["optionId"],
            "orderDetails.IncludeInOrder[0]": self.data["optionId"],
            "orderDetails.UnloadCargoOption": ""
        }
        logger.debug("Set info about delivery.")
        if self.data["AddressInfo"]["DeliveryWayCode"] == "self":
            info["address_self"] = self.data["AddressInfo"]["selectedAddressId"]
        elif self.data["AddressInfo"]["DeliveryWayCode"] == "courier":
            info["address_courier"] = self.data["AddressInfo"]["selectedAddressId"]
            info["orderDetails.DeliveryPrice"] = self.data["AddressInfo"]["DeliveryPrice"]

        url = "https://www.wildberries.ru/lk/basket/spa/submitorder"
        params = urllib.parse.urlencode(info)
        response = self.handle_request(
            method="POST",
            url=url,
            data=params
        )
        try:
            params = response["value"]["url"].split("?")[1]
        except (KeyError, IndexError):
            logger.error(f"Problems with payment:\n"
                         f"{response['value']}")
            print(response["value"])
        if self.order_verification(params):
            logger.info(f"Payment is successful:\n"
                        f"id object - {self.data['id_obj']}\n"
                        f"select card - {card}")
            print("Всё окей")

        else:
            logger.error(f"Problems with payment status\n"
                         f"id object - {self.data['id_obj']}\n"
                         f"select card - {card}")
            print("Что-то случилось со статусом оплаты заказа...")
        print(f"Заказ: {params}")
        logger.info(f"Successful order:\n"
                    f"id object - {self.data['id_obj']}\n"
                    f"select card - {card}")

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
            logger.debug(f"Get info about - {answ['id_obj']}")
            return answ
