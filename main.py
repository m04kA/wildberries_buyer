from pprint import pprint
from TG.Send_mesg_tg import *
import requests
import json
from Buyer_wb import *
import logging_conf
from DB_client import *


def main():
    # id товара, на котором тестируем.
    id_objkts = [24560782, 46618343, 46327106]
    my_test = Buyer_waildberries(
        cookies="A51CFBD3991DECA718F833712E74FF79983C17334EE62A335DE322EE6A48D9AAD2A2A7001406B99E8D5A204CE71608DF376F6ECD8684402D6593023B97F02A0447893FFEBC1DBC42642F3C7990F0B45D0A0AE05BE773B083338C79BC15070DF7A422CE1EE876D4C3A7DC46CB64D74042671B5FEEB8600098E69618BE41A69C7E70B6791049972EBF7CD39F9EE011D99C32E6AFE6642353AFAD1EFEFC03F2AF5E93AF6B201169C237242519A3FEA1A914C4873E4E510BD446DE4D82562A0F1B2B2E2944CD96E7697C7CFAE663426DF3B16A45C443CEB3F6703760B1CB129C9AA936198F0DD282D60341C02200E20FA6506E31531001671A81C440D031B6C83AC16AB59F6331B2B7765BB27B97139A9CE5E28A851DC003D3844A55F67176AA2A72D80DC249")

    for id_obj in id_objkts:
        data = my_test.stock_availability(my_test.nm_2_cards(id_obj))
        update_product(**data)
        if data["quantity"] > 0:
            send_message_info_item(data=data)

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
