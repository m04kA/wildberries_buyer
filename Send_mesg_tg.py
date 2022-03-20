import asyncio
import json
import time
import aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = aiogram.Bot(token='5270879131:AAF95EAuk0hH7r4Ga7P2UNWBoUBK7O8DDVI')
dp = aiogram.Dispatcher(bot, run_tasks_by_default=True)

# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_btn_2 = InlineKeyboardButton('Вторая кнопка!', callback_data='button2')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)

loop = asyncio.get_event_loop()
try:
    data = {
        'AddressInfo': {
            'DeliveryPrice': 199,
            'DeliveryWayCode': 'courier',
            'selectedAddressId': '7yJVe8E9jWnmHV5l1rvNN0WDOaM='
        },
        'id_obj': 31231133,
        'name': 'Чехол для телефона Samsung Galaxy A72 / Самсунг Гэлакси А72',
        'optionId': 68149834,
        'prise': 39,
        'quantity': 1
    }
    loop.run_until_complete(
        bot.send_message(764461859, f"```{json.dumps(data)}```", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton('Купить!', callback_data=f"buy.{data['optionId']}.{data['quantity']}")
        ]])))
except KeyboardInterrupt:
    loop.run_until_complete(bot.send_message(764461859, "Всего доброго"))
