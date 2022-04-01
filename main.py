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
    my_test = Buyer_waildberries(
        cookies="6B13CCBAAAAF2B6D3D6F7F2399E9028CAFC4D36CBB0672748A17A08F1B46542092C42D7BD6945D89075FDD93C55765DED51AA5C4DA3A06A4CE03CF662114C92C0D270C7D0ED7B7BA6AD388529C1DE3F18C9C6E1B6E1DCAED90656F7F2D25269DE698642A7BA7816039C15A73DAE681BEE8F4628F413F7659A2BD7D3BB5ED2F95A18FFD9AE56E3286037153D030E9D935F68E077AA31E30F9CC0D63C2E696D35749C7793C7A002B42D63BDACBF4EA6AFE19587F5E21721CD1A86F9C3AF311B9BE253C3509F531585B72ADF06F9806429ADDC4402F490E131B668800E5A65FED7D3D07B98AACE87941E959C93F4ED1C8FF3DCDCA9FD37F176AAA8F8FBE8F3EDDA6EE9EB0B29F33D4943BA7AFED44DA04F26B6D19383F4A6AA834A097B6E38B8966551E76B4"
    )
    for id_obj in id_objkts:
        data = my_test.stock_availability(my_test.nm_2_cards(id_obj))
        my_test.data = data
        update_product(obj=data['id_obj'], option=data["optionId"], name=data["name"], price=data["price"],
                       quantity=data["quantity"])
        if my_test.data["quantity"] > 0:
            send_message_info_item(data=my_test.data)
            # cards = my_test.info_about_cards(id_obj)
            # pprint(cards)
            # for key in cards.keys():
            #     print(f"{key} - {cards[key]}")  # Красивый вывод данных о картах
            # print('----------')
            # pprint(my_test.data)
            # flag = bool(int(input("Если нужно поменять карту, введите 1, иначе 0: ")))
            # print(my_test.data["quantity"])
            # if flag:
            #     name_card = input("Скопируйте и вставьте номер карты: ")
            #     flag = my_test.choosing_a_bank_card(name_bank_card=name_card, open_cards=cards)

            # if my_test.data["quantity"] > 0:
            #     flag = my_test.payment_by_card(cards)


if __name__ == "__main__":
    main()
