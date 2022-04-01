import asyncio
import json
import time
import aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = aiogram.Bot(token='5270879131:AAF95EAuk0hH7r4Ga7P2UNWBoUBK7O8DDVI')
dp = aiogram.Dispatcher(bot, run_tasks_by_default=True)


def send_message_info_item(data: dict = None, id_user: int = 764461859):
    """
    Функция отправки сообщения с кнопкой, предаставляющая возможность купить товар, который был в карточки.
    :param data:
    :param id_user:
    :return:
    """
    loop = asyncio.get_event_loop()
    try:
        if data:
            info = data
            loop.run_until_complete(
                bot.send_message(id_user, f"```{json.dumps(info)}```",
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                     InlineKeyboardButton('Купить!',
                                                          callback_data=f"buy.{data['id_obj']}.{data['quantity']}")
                                 ]]), parse_mode="MarkdownV2"))
        else:
            info = {'message': 'Data is none.'}
            loop.run_until_complete(bot.send_message(id_user, f"```{json.dumps(info)}```", parse_mode="MarkdownV2"))
        loop.close()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.send_message(id_user, "Всего доброго"))


def give_choice_card(open_cards: dict, id_user: int = 764461859):
    """
    Функция отправки сообщения с выбором карт.
    :param id_user: - id пользователя в ТГ
    :param open_cards: - Словарь с доступными картами.
    :return:
    """
    loop = asyncio.get_event_loop()
    try:
        key_board = InlineKeyboardMarkup(parse_mode="MarkdownV2")
        for number in open_cards.keys():
            button = InlineKeyboardButton(f"{number}", callback_data=f"{number}")
            key_board.add(button)

        loop.run_until_complete(
            bot.send_message(id_user, f"```{json.dumps(open_cards)}```",
                             reply_markup=key_board))
        loop.close()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.send_message(id_user, "Всего доброго"))
