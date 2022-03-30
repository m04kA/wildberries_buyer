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
        db = SqliteDatabase(name, pragmas={'foreign_keys': 1})

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


class Base_class(Model):
    """
    Базовый класс подключения к БД
    """

    class Meta:
        database = data_base


class Product(Base_class):
    """
    Модель товара хранит все необходимые параметры:
    :id: - Id товара
    :optionId: - Id заказа с товаром
    :name: - Название
    :price: - Цена
    :quantity: - Количество товара
    :last_update: - Последнее обновление записи
    """

    id_obj = PrimaryKeyField(null=False)
    optionId = IntegerField(null=False)
    name = CharField(null=True)
    price = BigIntegerField(null=True)
    quantity = IntegerField(null=True)
    last_update = DateTimeField(default=datetime.now())


Product.create_table()


class Cards(Base_class):
    """
    Модель банковских карт хранит все необходимые параметры:
    :number: - Номер карты
    :hash: - Хеш карты для wildberries
    :active: - Активная сейчас или отключена
    :last_update: - Последнее обновление записи
    """
    id = PrimaryKeyField(index=True, null=False)
    number = CharField(null=False)
    hash = CharField(null=False)
    active = BooleanField(null=False, default=False)
    last_update = DateTimeField(default=datetime.now())


Cards.create_table()


class Users(Base_class):
    """
    Модель пользователей, у которых будут свои корзины для заказа товаров.

    :id: - id Пользователя в ТГ
    """
    id = PrimaryKeyField(null=False, unique=True)
    last_update = DateTimeField(default=datetime.now())


Users.create_table()


class Order(Base_class):
    """
    Модель банковских карт хранит все необходимые параметры:
    :id: - id заказа
    :id_user: - id пользователя
    :id_obj: - id товара
    :last_update: - Последнее обновление записи
    """
    id = PrimaryKeyField(index=True)
    id_user = ForeignKeyField(Users.id, on_delete="cascade")
    id_obj = ForeignKeyField(Product.id_obj, on_delete="cascade")
    quantity = IntegerField(null=False, default=1)
    last_update = DateTimeField(default=datetime.now())


Order.create_table()


class Delivery(Base_class):
    id_order = ForeignKeyField(Order.id, null=True, on_delete="cascade")
    deliveryWayCode = CharField(null=False)
    selectedAddressId = CharField(null=False)
    deliveryPrice = CharField(default=None)


Delivery.create_table()


def update_product(id_obj: int, optionId: int = None, name: str = None, price: int = None, quantity: int = None):
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
        row: Product = Product.get(Product.id_obj == id_obj)
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


def get_product_info(id_obj: int) -> dict:
    """
    Получение данных о товаре из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param id_obj: - id продукта
    :return:
    """

    logger.debug(f"Get info about product (id_obj - {id_obj})")
    try:
        info = Product.select().where(
            Product.id_obj == id_obj
        ).get()
        if len(info):
            answ = {
                'id_obj': info.id_obj,
                'name': info.name,
                'optionId': info.optionId,
                'price': info.price,
                'quantity': info.quantity
            }
            return answ
    except Product.DoesNotExist as ex:
        logger.error(f"Product (id - {id_obj}) doesn`t exist.")
        print(f"Product (id - {id_obj}) doesn`t exist.")
        return {}


def delete_product(id_obj: int):
    logger.info(f"Delete product (id_obj - {id_obj})")
    product = Product.get(Product.id_obj == id_obj)
    product.delete_instance()


def update_card(number: str, hash: str = None, active: bool = None):
    """
    Обновление или добавление данных о товаре:
    :param number:  - Номер карты
    :param hash: - Хеш карты для wildberries
    :param active: - Активная сейчас или отключена
    :last_update: - Последнее обновление записи
    :return:
    """

    row: Cards = Cards.get(Cards.number == number)
    if hash:
        logger.info(f"Update name {row.hash} to {hash} (number card - {number})")
        row.hash = hash
    if active != None:
        logger.info(f"Update name {row.active} to {active} (number card - {number})")
        row.active = active
    if hash or active:
        row.last_update = datetime.datetime.now()
    logger.info(f'Create new product \n'
                f'number={number}, hash={hash}, active={active}')
    row = Cards.create(number=number, hash=hash, active=active)
    row.save()
    logger.info(f'Finish update operation with obj (number card - {number})')


def get_card_info(number: str) -> dict:
    """
    Получение данных по определённой карте
    :param number: - номер карты. который показывается в wildberries
    :return: - словарь с даными
    """
    logger.debug(f"Get info about bank card (number card - {number})")
    try:
        info = Cards.select().where(
            Cards.number == number
        ).dicts()
        logger.debug(f'Get info about card (number - {number})')
        return info
    except Cards.DoesNotExist:
        logger.error(f"Card (number - {number}) doesn`t exist.")
        print(f"Card (number - {number}) doesn`t exist.")
        return {}


def get_active_cards() -> list:
    """
    Выдаёт список всех активных карт на данный момент.
    :return:
    """
    logger.debug(f"Get info about bank cards (active == True)")
    try:
        cards = Cards.select().where(
            Cards.active == True
        ).get()
        return list(cards)
    except Cards.DoesNotExist:
        logger.error("Bank cards (active == True) doesn`t exist.")
        print("Bank cards (active == True) doesn`t exist.")
        return []


def delete_card(number: str):
    logger.info(f"Delete bank card (number - {number})")
    product = Cards.get(Cards.number == number)
    product.delete_instance()


def create_user(id: int):
    """
    Обновление или добавление данных о товаре:
    :param id:  - id пользователя
    """

    row = Users.create(id=id)
    row.save()
    logger.info(f'Finish update operation with obj (id_obj - {id})')


def get_user_info(id: int) -> dict:
    """
    Получение данных о пользователе из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param id: - id Пользователя
    :return:
    """
    logger.debug(f"Get info about user (id - {id})")
    try:
        info = Users.select().where(
            Users.id == id
        ).get()
        if len(info):
            answ = {
                'id': info.id,
            }
            return answ
    except Users.DoesNotExist:
        logger.error(f"User (id - {id}) doesn`t exist.")
        print(f"User (id - {id}) doesn`t exist.")
        return {}


def delete_user(id: int):
    logger.info(f"Delete user (id - {id})")
    product = Users.get(Product.id == id)
    product.delete_instance()


def update_order(id_user: int, id_obj: int, quantity: int = None):
    """
    Обновление или добавление данных о товаре:
    :param id_user:  - id_obj товара
    :param id_obj: - id_obj заказа с товаром
    :param quantity: - Количество товара
    :last_update: - Последнее обновление записи
    :return:
    """

    row: Order = Order.get(Order.id_user == id_user and Order.id_obj == id_obj)
    if quantity:
        logger.info(f"Update quantity {row.quantity} to {quantity} (id order - {row.id})")
        row.quantity = quantity
        row.last_update = datetime.now()

    row = Order.create(id=row.id, id_user=id_user, id_obj=id_obj, quantity=quantity)
    logger.info(f'Create new order \n'
                f'id={row.id}, id_user={id_user}, id_obj={id_obj}, quantity={quantity}')
    row.save()
    logger.info(f'Finish update operation with order (id order - {row.id})')


def get_order_info(id_user: int, id_obj: int) -> dict:
    """
    Получение данных о товаре из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param id_user: - id пользователя
    :param id_obj: - id продукта
    :return: - Словарь с данными по заказу
    """

    try:
        logger.debug(f"Get info about order (id_obj - {id_obj})")
        info: Order = Order.get(Order.id_user == id_user and Order.id_obj == id_obj)
        if len(info):
            answ = {
                'id': info.id,
                'id_user': info.id_user,
                'id_obj': info.id_obj,
                'quantity': info.quantity
            }
            return answ
    except Order.DoesNotExist:
        logger.error(f"Order (id_user - {id_user}; id_obj - {id_obj}) doesn`t exist.")
        print(f"Order (id_user - {id_user}; id_obj - {id_obj}) doesn`t exist.")
        return {}


def delete_order(id_user: int, id_obj: int):
    order: Order = Order.get(Order.id_user == id_user and Order.id_obj == id_obj)
    logger.info(f"Delete order (id - {order.id})")
    order.delete_instance()


def update_delivery(id_order: int, deliveryWayCode: str = None, selectedAddressId: str = None,
                    deliveryPrice: str = None):
    """
    Обновление или добавление данных о товаре:
    :param id_order:  - id заказа
    :param deliveryWayCode: - код доставки (self - пункт выдачи / courier - курьером)
    :param selectedAddressId: - id места доставки
    :param deliveryPrice: - Цена доставки при deliveryWayCode = courier
    :last_update: - Последнее обновление записи
    :return:
    """

    try:
        row: Delivery = Delivery.get(Delivery.id_order == id_order)
        if deliveryWayCode:
            logger.info(
                f"Update deliveryWayCode {row.deliveryWayCode} to {deliveryWayCode} (id order - {row.id_order})")
            row.deliveryWayCode = deliveryWayCode
        if selectedAddressId:
            logger.info(
                f"Update selectedAddressId {row.selectedAddressId} to {selectedAddressId} (id order - {row.id_order})")
            row.selectedAddressId = selectedAddressId
        if deliveryPrice:
            logger.info(f"Update selectedAddressId {row.deliveryPrice} to {deliveryPrice} (id order - {row.id_order})")
            row.deliveryPrice = deliveryPrice
        if deliveryWayCode or selectedAddressId or deliveryPrice:
            row.last_update = datetime.now()
    except DoesNotExist:
        row = Delivery.create(id_order=row.id_order, deliveryWayCode=deliveryWayCode,
                              selectedAddressId=selectedAddressId, deliveryPrice=deliveryPrice)
        logger.info(f'Create new order \n'
                    f'id_order={row.id_order}, deliveryWayCode={deliveryWayCode}, selectedAddressId={selectedAddressId}, deliveryPrice={deliveryPrice}')
    row.save()
    logger.info(f'Finish update operation with delivery (id_order - {id_order})')


def get_delivery_info(id_order: int) -> dict:
    """
    Получение данных о товаре из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param id_order: - id заказа
    :return: - Словарь с данными по заказу
    """

    try:
        logger.debug(f"Get info about delivery (id order - {id_order})")
        info: Delivery = Delivery.get(Delivery.id_order == id_order)
        if len(info):
            answ = {
                'id_order': info.id_order,
                'deliveryWayCode': info.deliveryWayCode,
                'selectedAddressId': info.selectedAddressId,
                'deliveryPrice': info.deliveryPrice
            }
            return answ
    except Delivery.DoesNotExist:
        logger.error(f"Delivery for order (id_order - {id_order}) doesn`t exist.")
        print(f"Delivery for order (id_order - {id_order}) doesn`t exist.")
        return {}


def delete_order(id_order: int):
    delivery: Delivery = Order.get(Delivery.id_order == id_order)
    logger.info(f"Delete order (id - {delivery.id_order})")
    delivery.delete_instance()


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
data = get_product_info(31231135)
print("---------")
print(data)
print("---------")
