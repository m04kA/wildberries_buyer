from pprint import pprint

from DataBase.plagins import *

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





# update_product(
#     obj=31231136,
#     option=68149834,
#     name='Чехол для телефона Samsung Galaxy A72 / Самсунг Гэлакси А72',
#     price=39,
#     quantity=2
# )
# create_user(id=11)

# update_card(
#     user=12,
#     number='427638******8131',
#     hash='f598cbdd-a2a6-11ec-a146-964d458f538c',
#     select=True,
#     active=True
# )

# delete_card(12, "427638******8131")

# gg = get_active_cards(11)
# pprint(gg)
# update_card(
#     user=11,
#     number='553691******7412',
#     hash='25db25af-9fb9-11ec-ad1b-02adff0c675e',
#     select=False,
#     active=True
# )

# update_card(
#     user=11,
#     number='777766******7777',
#     hash='25db25af-9fb9-11ec-ad1b-02adff0cyyyyy',
#     select=False,
#     active=False
# )

# update_order(user=11, obj=31231136, quantity=2)
#
# ord = get_order_info(11, 31231136)
#
# if ord:
#     update_delivery(order_id=ord["id"], delivery_way_code="self", selected_address_id="161616")
#
# # data = get_order_info(11, 31231136)
# print("---------")
# print(ord)
# print("---------")
