from datetime import datetime, timedelta
from peewee import *
from loguru import logger

config_base = {
    "type": "sqlite3",
    "dbname": "wildberries",
    "user": "",
    "password": "",
    "host": "",
    "port": ""
}


"""
Данные для тестирования...
{'427638******8131': {'id': 'f598cbdd-a2a6-11ec-a146-964d458f538c',
                      'select': True,
                      'system': 'visa'},
 '553691******7412': {'id': '25db25af-9fb9-11ec-ad1b-02adff0c675e',
                      'select': False,
                      'system': 'mastercard'}}
----------
{'AddressInfo': {'DeliveryPrice': 199,
                 'DeliveryWayCode': 'courier',
                 'selectedAddressId': '7yJVe8E9jWnmHV5l1rvNN0WDOaM='},
 'id_obj': 31231133,
 'name': 'Чехол для телефона Samsung Galaxy A72 / Самсунг Гэлакси А72',
 'optionId': 68149834,
 'prise': 39,
 'quantity': 1}

Process finished with exit code 0
"""


def get_base_client():
    """
    Подключает клиент базы данных по настройкам,
    заданным в файле.
    :path: - Путь файла конфигураций

    Обязательными полями являются параметры:
    :type: - один из типов 'sqlite3', 'mysql'
    :dbname: - название базы данных
    Для MySQL должны быть указаны параметры:
    :user: - логин
    :password: - пароль
    :host: - хост
    :port: - порт

    Возвратит один из двух клиентов(SQLite3, MySql).
    В случае несоответствия параметров вызовет Exception/
    :return:
    """

    base = config_base

    if base['type'] == 'sqlite3':
        name = f'{base["dbname"]}.{base["type"]}'
        db = SqliteDatabase(name)

    elif base['type'] == 'mysql':
        db = MySQLDatabase(
            base['dbname'],
            user=base['user'],
            password=base['password'],
            host=base['host'],
            port=base['port'],
        )
    else:
        raise Exception
    return db


data_base = get_base_client()


class Product(Model):
    """
    Модель товара хранит все необходимые параметры:
    :id: - Id товара
    :optionId: - Id заказа с товаром
    :name: - Название
    :price: - Цена
    :quantity: - Количество товара
    :last_update: - Последнее обновление записи
    """

    id = IntegerField(null=False)
    optionId = IntegerField(null=False)
    name = CharField(null=True)
    price = BigIntegerField(null=True)
    quantity = IntegerField(null=True)
    last_update = DateTimeField(default=datetime.now())

    class Meta:
        database = data_base


class Cards(Model):
    """
    Модель банковских карт хранит все необходимые параметры:
    :number: - Номер карты
    :hash: - Хеш карты для wildberries
    :active: - Активная сейчас или отключена
    :last_update: - Последнее обновление записи
    """
    number = CharField(null=False)
    hash = CharField(null=False)
    active = BooleanField(null=False, default=False)
    last_update = DateTimeField(default=datetime.now())

    class Meta:
        database = data_base


def update_product(id, optionId: int = None, name: str = None, price: int = None, quantity: int = None):
    """
    Обновление или добавление данных о товаре:
    :param id:  - Id товара
    :param optionId: - Id заказа с товаром
    :param name: - Название
    :param price: - Цена
    :param quantity: - Количество товара
    :last_update: - Последнее обновление записи
    :return:
    """

    try:
        row = Product.get(Product.id == id)
        if optionId:
            row.optionId = optionId
        if name:
            row.name = name
        if price:
            row.price = price
        if quantity:
            row.stock = quantity
        if name or price or quantity:
            row.last_update = datetime.datetime.now()
    except DoesNotExist:
        row = Product.create(id=id, optionId=optionId, name=name, price=price, quantity=quantity)
    row.save()


def update_card(number: str, hash: str = None, active: bool = None):
    """
    Обновление или добавление данных о товаре:
    :param number:  - Номер карты
    :param hash: - Хеш карты для wildberries
    :param active: - Активная сейчас или отключена
    :last_update: - Последнее обновление записи
    :return:
    """

    try:
        row = Cards.get(Cards.number == number)
        if hash:
            row.hash = hash
        if active != None:
            row.active = active
        if hash or active:
            row.last_update = datetime.datetime.now()
    except DoesNotExist:
        row = Cards.create(number=number, hash=hash, active=active)
    row.save()


def get_product_info(id: int) -> dict:
    """
    Получение данных о товаре из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param id: id товара
    :return:
    """

    info = Product.select().where(
        Product.id == id
    ).dicts()
    return info


def get_card_info(number: str) -> dict:
    """
    Получение данных по определённой карте
    :param number: - номер карты. который показывается в wildberries
    :return: - словарь с даными
    """
    info = Cards.select().where(
        Cards.number == number
    ).dicts()
    return info


def get_active_cards() -> list:
    """
    Выдаёт список всех активных карт на данный момент.
    :return:
    """
    cards = Cards.select().where(
        Cards.active == True
    ).dicts()
    return list(cards)
