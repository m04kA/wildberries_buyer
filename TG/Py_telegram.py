import asyncio
import time
import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.utils.helper import Helper, HelperMode, ListItem


class TestStates(Helper):
    mode = HelperMode.snake_case

    TEST_STATE_0 = ListItem()


bot = aiogram.Bot(token='5270879131:AAF95EAuk0hH7r4Ga7P2UNWBoUBK7O8DDVI')
dp = aiogram.Dispatcher(bot, run_tasks_by_default=True, storage=MemoryStorage())

data_users = {}



@dp.message_handler(content_types=['text', 'document', 'audio'])
@dp.message_handler(state="*", commands=['help, start'])
async def get_text_messages(message: aiogram.types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == "/start" or message.text == "/help":
        await bot.send_message(message.from_user.id,
                               "Если хотите провести закупку, нажмите кнопку, и следуйте инструкциям.")
        await state.set_state(TestStates.all()[0])
    else:
        await state.reset_state()
        await message.answer("Введите /help")


@dp.callback_query_handler()
async def process_callback_button1(callback_query: aiogram.types.CallbackQuery):
    global data_users
    state = dp.current_state(user=callback_query.from_user.id)  # ?
    callback_data = callback_query.data.split('.')
    if callback_data[0] == 'buy':
        await bot.answer_callback_query(callback_query.id)  # ?
        await bot.send_message(callback_query.from_user.id,
                               f'В каком количестве вы хотите купить товар (id - {callback_data[1]})\n'
                               f'Максимум можно купить {callback_data[2]}')

        data_users[callback_query.from_user] = {
            "id_obj": int(callback_data[1]),
            "quantity": int(callback_data[2])
        }

        await state.set_state(TestStates.all()[0])

    else:
        await state.reset_state()
        await callback_query.answer("Введите /help")


@dp.message_handler(state=TestStates.TEST_STATE_0)
async def buy(message: aiogram.types.Message):
    global data_users
    state = dp.current_state(user=message.from_user.id)
    if not message.text.isdigit():
        await message.answer("Ошибочный ввод\n"
                             "Введите количество товара товара: ")
    elif int(message.text) <= 0 or int(message.text) > data_users[message.from_user]["quantity"]:
        await message.answer("Ошибочный ввод\n"
                             "Введите количество товара товара: ")
    else:
        data_users[message.from_user]["quantity"] = int(message.text)
        cards = my_test.info_about_cards(id_obj)
        pprint(cards)
        await state.reset_state()
        del data_users[message.from_user]


executor = aiogram.executor.Executor(
    loop=asyncio.get_event_loop(),
    skip_updates=[],
    dispatcher=dp,
)
executor.start_polling()
