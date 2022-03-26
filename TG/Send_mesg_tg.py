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
    # start = time.time()
    # while True:
    loop = asyncio.get_event_loop()
    try:
        if data:
            info = data
            loop.run_until_complete(
                bot.send_message(id_user, f"```{json.dumps(info,ensure_ascii=False)}```",
                                 reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                     InlineKeyboardButton('Купить!',
                                                          callback_data=f"buy.{data['optionId']}.{data['quantity']}")
                                 ]]), parse_mode="MarkdownV2"))
        else:
            info = {
                'message': 'Data is none.'}
            loop.run_until_complete(bot.send_message(id_user, f"```{json.dumps(info,ensure_ascii=False)}```", parse_mode="MarkdownV2"))
            print(0)
        # time.sleep(15)
    except KeyboardInterrupt:
        loop.run_until_complete(bot.send_message(764461859, "Всего доброго"))
        # if time.time() - start > 31:
        #     break

# send_message_info_item()
