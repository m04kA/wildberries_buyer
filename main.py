from pprint import pprint
from TG.Send_mesg_tg import *
import requests
import json
from Buyer_wb import *
from DataBase.plagins import *
import logging_conf


def main():
    # id товара, на котором тестируем.
    id_objkts = [24560782, 46618343, 46327106]
    my_test = Buyer_waildberries()

    for id_obj in id_objkts:
        data = my_test.stock_availability(my_test.nm_2_cards(id_obj))
        my_test.data = data
        update_product(obj=data['id_obj'], option=data["optionId"], name=data["name"], price=data["price"],
                       quantity=data["quantity"])
        if my_test.data["quantity"] > 0:
            send_message_info_item(data=my_test.data)
            cards = my_test.info_about_cards(id_obj)
            pprint(cards)
            # for key in cards.keys():
            #     print(f"{key} - {cards[key]}")  # Красивый вывод данных о картах
            print('----------')
            pprint(my_test.data)
            flag = bool(int(input("Если нужно поменять карту, введите 1, иначе 0: ")))
            print(my_test.data["quantity"])
            if flag:
                name_card = input("Скопируйте и вставьте номер карты: ")
                flag = my_test.choosing_a_bank_card(name_bank_card=name_card, open_cards=cards)

            # if my_test.data["quantity"] > 0:
            #     flag = my_test.payment_by_card(cards)


if __name__ == "__main__":
    main()
