from pprint import pprint
from TG.Send_mesg_tg import *
import requests
import json
from Buyer_wb import *
from DataBase.plagins import *
import logging_conf


def main():
    # id товара, на котором тестируем.
    id_objkts = [13617000, 61209916, 46327106]
    my_test = Buyer_waildberries(
        cookies="0E8FFE6C3B71611AF60A38FF71D2E4ED4ECAF447A0B45319F760AAF0AC511D32E482213B904961E1606841E81C73B8FF3BA22962F22A55EF5BBE56EA92306720F0EE5808E573B681E3C5FD6A20E6DBF6C25B4F1585DAF63A5D015CEAE79DA5881FB40823882033D92F354713F482707361E4C0FB27965036079B9586916F864B522F28FC0E528A80289C3D907AD95F19B3E87FD61977AA175917F3BAE3961922FF768CCD8F2F4966A5AF4DC8F5EEB3D005EC2DF40D06C8413241F8B563DD39B487C3AD0F3C577440FBB4445765EE13DDF7CCA525268506CC7AC4637D8B4CEDDB79BE1E7287BCCE7EB4D0F93BEDAE586FEEC2EB9314967CDDAB80BDB2B4D3D59AD02BF1918B4360D335005F62194D374533A40486553BAE8EABF1DFB4D77566F6638886EB"
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
        else:
            print(f"Товар {my_test.data['name']} (id - {my_test.data['id_obj']}) отсутствует")
            logger.info(f"Object {my_test.data['name']} (id - {my_test.data['id_obj']}) does not exist.")


if __name__ == "__main__":
    main()
