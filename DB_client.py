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


logger.info(f"Connect to data base {config_base['dbname']}")
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

    id_obj = IntegerField(null=False)
    optionId = IntegerField(null=False)
    name = CharField(null=True)
    price = BigIntegerField(null=True)
    quantity = IntegerField(null=True)
    last_update = DateTimeField(default=datetime.now())

    class Meta:
        database = data_base


Product.create_table()


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


Cards.create_table()


class Delivery(Model):
    """
    Модель банковских карт хранит все необходимые параметры:
    :number: - Номер карты
    :hash: - Хеш карты для wildberries
    :active: - Активная сейчас или отключена
    :last_update: - Последнее обновление записи
    """
    id = ForeignKeyField()
    hash = CharField(null=False)
    active = BooleanField(null=False, default=False)
    last_update = DateTimeField(default=datetime.now())

    class Meta:
        database = data_base


Cards.create_table()


def update_product(id_obj, optionId: int = None, name: str = None, price: int = None, quantity: int = None):
    """
    Обновление или добавление данных о товаре:
    :param id_obj:  - id_obj товара
    :param optionId: - id_obj заказа с товаром
    :param name: - Название
    :param price: - Цена
    :param quantity: - Количество товара
    :last_update: - Последнее обновление записи
    :return:
    """

    try:
        row = Product.get(Product.id_obj == id_obj)
        if optionId:
            logger.info(f"Update optionId {row.optionId} to {optionId} (id_obj object - {id_obj})")
            row.optionId = optionId
        if name:
            logger.info(f"Update name {row.name} to {name} (id_obj object - {id_obj})")
            row.name = name
        if price:
            logger.info(f"Update name {row.price} to {price} (id_obj object - {id_obj})")
            row.price = price
        if quantity:
            logger.info(f"Update name {row.quantity} to {quantity} (id_obj object - {id_obj})")
            row.quantity = quantity
        if name or price or quantity:
            row.last_update = datetime.now()
    except DoesNotExist:
        logger.info(f'Create new product \n'
                    f'id_obj={id_obj}, optionId={optionId}, name={name}, price={price}, quantity={quantity}')
        row = Product.create(id_obj=id_obj, optionId=optionId, name=name, price=price, quantity=quantity)
    row.save()
    logger.info(f'Finish update operation with obj (id_obj - {id_obj})')


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
            logger.info(f"Update name {row.hash} to {hash} (number card - {number})")
            row.hash = hash
        if active != None:
            logger.info(f"Update name {row.active} to {active} (number card - {number})")
            row.active = active
        if hash or active:
            row.last_update = datetime.datetime.now()
    except DoesNotExist:
        logger.info(f'Create new product \n'
                    f'number={number}, hash={hash}, active={active}')
        row = Cards.create(number=number, hash=hash, active=active)
    row.save()
    logger.info(f'Finish update operation with obj (number card - {number})')


def get_product_info(id_obj: int) -> dict:
    """
    Получение данных о товаре из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param id: id товара
    :return:
    """

    logger.debug(f"Get info about product (id_obj - {id_obj})")
    info = Product.select().where(
        Product.id_obj == id_obj
    )
    if len(info):
        answ = {
            'id_obj': info.id_obj,
            'name': info.name,
            'optionId': info.optionId,
            'price': info.price,
            'quantity': info.quantity
        }
        return answ
    return {}


# comment

def get_card_info(number: str) -> dict:
    """
    Получение данных по определённой карте
    :param number: - номер карты. который показывается в wildberries
    :return: - словарь с даными
    """
    logger.debug(f"Get info about bank card (number card - {number})")
    info = Cards.select().where(
        Cards.number == number
    ).dicts()
    logger.debug(f'get info')
    return info


def get_active_cards() -> list:
    """
    Выдаёт список всех активных карт на данный момент.
    :return:
    """
    logger.debug(f"Get info about bank cards (active == True)")
    cards = Cards.select().where(
        Cards.active == True
    ).dicts()
    return list(cards)


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
update_product(
    id_obj=31231134,
    optionId=68149834,
    name='Чехол для телефона Samsung Galaxy A72 / Самсунг Гэлакси А72',
    price=39,
    quantity=2
)
data = get_product_info(31231134)
print("---------")
print(data)
print("---------")

