import requests
import json
from Buyer_wb import *


def main():
    # id товара, на котором тестируем.
    id_obj = 25349771
    my_test = Buyer_waildberries()
    cards, data = my_test.info_about_cards(id_obj)
    for key in cards.keys():
        print(f"{key} - {cards[key]}")  # Красивый вывод данных о картах
    flag = bool(int(input("Если нужно поменять карту, введите 1, иначе 0: ")))
    if flag:
        name_card = input("Скопируйте и вставьте номер карты: ")
        flag = my_test.choosing_a_bank_card(name_bank_card=name_card, open_cards=cards, data=data)

    # Проверка на отработку всего.
    if flag:
        print(1)
    else:
        print(0)


if __name__ == "__main__":
    main()
