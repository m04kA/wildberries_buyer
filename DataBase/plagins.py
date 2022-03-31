from datetime import datetime, timedelta

import peewee
from peewee import *
from loguru import logger
from DataBase.DB_client import *


def update_product(obj: int, option: int = None, name: str = None, price: int = None, quantity: int = None):
    """
    Обновление или добавление данных о товаре:
    :param obj:  - id_obj товара
    :param option: - id_obj заказа с товаром
    :param name: - Название
    :param price: - Цена
    :param quantity: - Количество товара
    :last_update: - Последнее обновление записи
    :return:
    """

    try:
        row: Product = Product.get(Product.obj == obj)
        if option:
            logger.info(f"Update option {row.option} to {option} (obj object - {obj})")
            row.option = option
        if name:
            logger.info(f"Update name {row.name} to {name} (obj object - {obj})")
            row.name = name
        if price:
            logger.info(f"Update name {row.price} to {price} (obj object - {obj})")
            row.price = price
        if quantity:
            logger.info(f"Update name {row.quantity} to {quantity} (obj object - {obj})")
            row.quantity = quantity
        if name or price or quantity:
            row.last_update = datetime.now()
    except Product.DoesNotExist:
        logger.info(f'Create new product \n'
                    f'obj={obj}, option={option}, name={name}, price={price}, quantity={quantity}')
        row = Product.create(obj=obj, option=option, name=name, price=price, quantity=quantity)
    row.save()
    logger.info(f'Finish update operation with obj (obj - {obj})')


def get_product_info(obj: int) -> dict:
    """
    Получение данных о товаре из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param obj: - id продукта
    :return:
    """

    logger.debug(f"Get info about product (obj - {obj})")
    try:
        info: Product = Product.get(Product.obj == obj)
        answ = {
            'obj': info.obj,
            'option': info.option,
            'name': info.name,
            'price': info.price,
            'quantity': info.quantity
        }
        return answ
    except Product.DoesNotExist:
        logger.error(f"Product (id - {obj}) doesn`t exist.")
        print(f"Product (id - {obj}) doesn`t exist.")
        return {}


def delete_product(obj: int):
    logger.info(f"Delete product (obj - {obj})")
    try:
        product = Product.get(Product.obj == obj)
        product.delete_instance()
    except Product.DoesNotExist:
        logger.info(f"Error delete product (obj - {obj})")


def update_card(user: int, number: str, hash: str = None, select: bool = None, active: bool = None):
    """
    Обновление или добавление данных о товаре:
    :param user: - Пользователь, которому доступна эта карта
    :param select: - Выбрана ли карта
    :param number:  - Номер карты
    :param hash: - Хеш карты для wildberries
    :param active: - Активная сейчас или отключена
    :last_update: - Последнее обновление записи
    :return:
    """

    try:
        row = Cards.select().where((Cards.user == user) & (Cards.number == number)).get()
        if hash:
            logger.info(f"Update hash {row.hash} to {hash} (number card - {number})")
            row.hash = hash
        if select:
            logger.info(f"Update select {row.select} to {select} (number card - {number})")
            row.select = select
        if active != None:
            logger.info(f"Update active {row.active} to {active} (number card - {number})")
            row.active = active
        if hash or active or select:
            row.last_update = datetime.now()
        logger.info(f'Create new card \n'
                    f'number={number}, hash={hash}, active={active}')
    except Cards.DoesNotExist:
        row = Cards.create(user=user, number=number, hash=hash, select=select, active=active)
    row.save()
    logger.info(f'Finish update operation with obj (number card - {number})')


def get_card_info(user: int, number: str) -> dict:
    """
    Получение данных по определённой карте
    :param user: - Пользователь, которому доступна эта карта
    :param number: - номер карты. который показывается в wildberries
    :return: - словарь с даными
    """
    logger.debug(f"Get info about bank card (number card - {number})")
    answer = {}
    try:
        info: Cards = Cards.select().where((Cards.number == number) & (Cards.user == user))
        logger.debug(f'Get info about card (number - {number})')
        answer = {
            'id': info.id,
            'user': info.user,
            'number': info.number,
            'hash': info.hash,
            'select': info.select,
            'active': info.active
        }
    except Cards.DoesNotExist:
        logger.error(f"Card (number - {number}) doesn`t exist.")
        print(f"Card (number - {number}) doesn`t exist.")
    return answer


def get_active_cards(user: int) -> list:
    """
    Выдаёт список всех активных карт на данный момент.
    :param user: - Пользователь, которому доступны карты
    :return:
    """
    answer = []
    logger.debug(f"Get info about bank cards (active == True)")
    try:
        cards = Cards.select().where(Cards.active == True & Cards.user == user)
        for card in cards:
            answer.append(get_card_info(card.user, card.number))
    except Cards.DoesNotExist:
        logger.error("Bank cards (active == True) doesn`t exist.")
        print("Bank cards (active == True) doesn`t exist.")
    return answer


def delete_card(user: int, number: str):
    logger.info(f"Delete bank card (number - {number})")
    try:
        product = Cards.select().where(Cards.number == number & Cards.user == user).get()
        product.delete_instance()
    except Cards.DoesNotExist:
        logger.error(f"Error delete card (number - {number}) -> does not exist.")


def create_user(id: int):
    """
    Обновление или добавление данных о товаре:
    :param id:  - id пользователя
    """
    user = get_user_info(id)
    if not user:
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
    answ = {}
    logger.debug(f"Get info about user (id - {id})")
    try:
        info = Users.select().where(
            Users.id == id
        ).get()
        answ = {
            'id': info.id,
        }
    except Users.DoesNotExist:
        logger.error(f"User (id - {id}) doesn`t exist.")
        print(f"User (id - {id}) doesn`t exist.")
    return answ


def delete_user(id: int):
    logger.info(f"Delete user (id - {id})")
    try:
        product = Users.get(Product.id == id)
        product.delete_instance()
    except Users.DoesNotExist:
        logger.error(f"Can`t delete user (id - {id}) doesn`t exist.")


def update_order(user: int, obj: int, quantity: int = None):
    """
    Обновление или добавление данных о товаре:
    :param user:  - obj товара
    :param obj: - obj заказа с товаром
    :param quantity: - Количество товара
    :last_update: - Последнее обновление записи
    :return:
    """
    try:
        row: Order = Order.select().where((Order.user == user) & (Order.obj == obj)).get()
        if quantity:
            logger.info(f"Update quantity {row.quantity} to {quantity} (id order - {row.id})")
            row.quantity = quantity
            row.last_update = datetime.now()
    except Order.DoesNotExist:
        row = Order.create(user=user, obj=obj, quantity=quantity)
        logger.info(f'Create new order \n'
                    f'id={row.id}, user={user}, obj={obj}, quantity={quantity}')
    row.save()
    logger.info(f'Finish update operation with order (id order - {row.id})')


def get_order_info(user: int, obj: int) -> dict:
    """
    Получение данных о товаре из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param user: - id пользователя
    :param obj: - id продукта
    :return: - Словарь с данными по заказу
    """
    answ = {}
    try:
        logger.debug(f"Get info about order (obj - {obj})")
        info: Order = Order.select().where((Order.user == user) & (Order.obj == obj)).get()
        answ = {
            'id': info.id,
            'user': info.user_id,
            'obj': info.obj_id,
            'quantity': info.quantity
        }

    except Order.DoesNotExist as ex:
        print(ex)
        print(info)
        logger.error(f"Order (user - {user}; obj - {obj}) doesn`t exist.")
        print(f"Order (user - {user}; obj - {obj}) doesn`t exist.")
    return answ


def delete_order(user: int, obj: int):
    try:
        order: Order = Order.get(Order.user == user and Order.obj == obj)
        logger.info(f"Delete order (id - {order.id})")
        order.delete_instance()
    except Order.DoesNotExist:
        logger.info(f"Error delete order (id - {order.id}) does not exist.")


def update_delivery(order_id: int, delivery_way_code: str = None, selected_address_id: str = None,
                    delivery_price: str = None):
    """
    Обновление или добавление данных о товаре:
    :param order_id:  - id заказа
    :param delivery_way_code: - код доставки (self - пункт выдачи / courier - курьером)
    :param selected_address_id: - id места доставки
    :param delivery_price: - Цена доставки при delivery_way_code = courier
    :last_update: - Последнее обновление записи
    :return:
    """

    try:
        row: Delivery = Delivery.get(Delivery.order_id == order_id)
        if delivery_way_code:
            logger.info(
                f"Update delivery_way_code {row.delivery_way_code} to {delivery_way_code} (id order - {row.order_id})")
            row.delivery_way_code = delivery_way_code
        if selected_address_id:
            logger.info(
                f"Update selected_address_id {row.selected_address_id} to {selected_address_id} (id order - {row.order_id})")
            row.selected_address_id = selected_address_id
        if delivery_price:
            logger.info(
                f"Update selected_address_id {row.delivery_price} to {delivery_price} (id order - {row.order_id})")
            row.delivery_price = delivery_price
        if delivery_way_code or selected_address_id or delivery_price:
            row.last_update = datetime.now()
    except Delivery.DoesNotExist:
        row = Delivery.create(order_id=order_id, delivery_way_code=delivery_way_code,
                              selected_address_id=selected_address_id, delivery_price=delivery_price)
        logger.info(f'Create new order \n'
                    f'order_id={row.order_id}, delivery_way_code={delivery_way_code}, selected_address_id={selected_address_id}, delivery_price={delivery_price}')
    row.save()
    logger.info(f'Finish update operation with delivery (order_id - {order_id})')


def get_delivery_info(order_id: int) -> dict:
    """
    Получение данных о товаре из таблицы в БД:
    Возвращает список словарей со всеми параметрами
    :param order_id: - id заказа
    :return: - Словарь с данными по заказу
    """

    try:
        logger.debug(f"Get info about delivery (id order - {order_id})")
        info: Delivery = Delivery.get(Delivery.order_id == order_id)

        answ = {
            'order_id': info.order_id,
            'delivery_way_code': info.delivery_way_code,
            'selected_address_id': info.selected_address_id,
            'delivery_price': info.delivery_price
        }
        return answ
    except Delivery.DoesNotExist:
        logger.error(f"Delivery for order (order_id - {order_id}) doesn`t exist.")
        print(f"Delivery for order (order_id - {order_id}) doesn`t exist.")
        return {}


def delete_order(order_id: int):
    try:
        delivery: Delivery = Order.get(Delivery.order_id == order_id)
        logger.info(f"Delete order (id - {delivery.order_id})")
        delivery.delete_instance()
    except Order.DoesNotExist:
        logger.info(f"Error delete order (id - {delivery.order_id}) does not exist")
