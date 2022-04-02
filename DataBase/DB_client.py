from datetime import datetime, timedelta

import peewee
from peewee import *
from loguru import logger
from DataBase import *


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

    obj = PrimaryKeyField(null=False)
    option = IntegerField(null=False)
    name = CharField(null=True)
    price = BigIntegerField(null=True)
    quantity = IntegerField(null=True)
    last_update = DateTimeField(default=datetime.now())


Product.create_table()


class Users(Base_class):
    """
    Модель пользователей, у которых будут свои корзины для заказа товаров.

    :id: - id Пользователя в ТГ
    """
    id = PrimaryKeyField(null=False, unique=True)
    last_update = DateTimeField(default=datetime.now())


Users.create_table()


class Cards(Base_class):
    """
    Модель банковских карт хранит все необходимые параметры:
    :number: - Номер карты
    :user: - id пользователя, которому доступны эта карта
    :hash: - Хеш карты для wildberries
    :active: - Активная сейчас или отключена
    :last_update: - Последнее обновление записи
    """
    id = PrimaryKeyField(index=True, null=False)
    user = ForeignKeyField(Users.id, null=False, on_delete="cascade")
    number = CharField(null=False)
    hash = CharField(null=False)
    select = BooleanField(null=False, default=False)
    active = BooleanField(null=False, default=False)
    last_update = DateTimeField(default=datetime.now())


Cards.create_table()


class Order(Base_class):
    """
    Модель банковских карт хранит все необходимые параметры:
    :id: - id заказа
    :id_user: - id пользователя
    :id_obj: - id товара
    :last_update: - Последнее обновление записи
    """
    id = PrimaryKeyField(index=True)
    user = ForeignKeyField(Users.id, on_delete="cascade")
    obj = ForeignKeyField(Product.obj, on_delete="cascade")
    quantity = IntegerField(null=False, default=1)
    last_update = DateTimeField(default=datetime.now())


Order.create_table()


class Delivery(Base_class):
    order = ForeignKeyField(Order.id, null=False, on_delete="cascade")
    delivery_way_code = CharField(null=False)
    selected_address_id = CharField(null=False)
    delivery_price = CharField(null=True)


Delivery.create_table()
