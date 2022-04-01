import asyncio
import time
import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Buyer_wb import *
from DataBase.plagins import *
from aiogram.utils.helper import Helper, HelperMode, ListItem
from TG.Send_mesg_tg import give_choice_card


class TestStates(Helper):
    mode = HelperMode.snake_case

    BUY_PRODUCT_2 = ListItem()
    CHOICE_CARD_1 = ListItem()
    QUANTITY_0 = ListItem()


bot = aiogram.Bot(token='5270879131:AAF95EAuk0hH7r4Ga7P2UNWBoUBK7O8DDVI')
dp = aiogram.Dispatcher(bot, run_tasks_by_default=True, storage=MemoryStorage())

waildberries_b = Buyer_waildberries(
    cookies="6B13CCBAAAAF2B6D3D6F7F2399E9028CAFC4D36CBB0672748A17A08F1B46542092C42D7BD6945D89075FDD93C55765DED51AA5C4DA3A06A4CE03CF662114C92C0D270C7D0ED7B7BA6AD388529C1DE3F18C9C6E1B6E1DCAED90656F7F2D25269DE698642A7BA7816039C15A73DAE681BEE8F4628F413F7659A2BD7D3BB5ED2F95A18FFD9AE56E3286037153D030E9D935F68E077AA31E30F9CC0D63C2E696D35749C7793C7A002B42D63BDACBF4EA6AFE19587F5E21721CD1A86F9C3AF311B9BE253C3509F531585B72ADF06F9806429ADDC4402F490E131B668800E5A65FED7D3D07B98AACE87941E959C93F4ED1C8FF3DCDCA9FD37F176AAA8F8FBE8F3EDDA6EE9EB0B29F33D4943BA7AFED44DA04F26B6D19383F4A6AA834A097B6E38B8966551E76B4"
)


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
    state = dp.current_state(user=callback_query.from_user.id)  # ?
    callback_data = callback_query.data.split('.')
    if callback_data[0] == 'buy':
        # await bot.answer_callback_query(callback_query.id)  # ?
        await bot.send_message(callback_query.from_user.id,
                               f'В каком количестве вы хотите купить товар (id - {callback_data[1]})\n'
                               f'Максимум можно купить {callback_data[2]}')

        create_user(int(callback_query.from_user))
        resp = waildberries_b.nm_2_cards(int(callback_data[1]))
        waildberries_b.data = waildberries_b.stock_availability(resp)

        await state.set_state(TestStates.QUANTITY_0[0])

    else:
        await state.reset_state()
        await callback_query.answer("Введите /help")


@dp.message_handler(state=TestStates.QUANTITY_0[0])
async def buy(message: aiogram.types.Message):
    state = dp.current_state(user=message.from_user.id)
    if not message.text.isdigit():
        await message.answer("Ошибочный ввод\n"
                             "Введите количество товара товара: ")
    elif int(message.text) <= 0 or int(message.text) > waildberries_b.data["quantity"]:
        await message.answer("Ошибочный ввод\n"
                             "Введите количество товара товара: ")
    else:
        quantity = int(message.text)
        update_order(user=int(message.from_user.id), obj=waildberries_b.data['id_obj'], quantity=quantity)
        cards_right = waildberries_b.info_about_cards(waildberries_b.data['id_obj'], quantity=quantity)
        for name, value in cards_right.items():
            update_card(user=int(message.from_user.id), number=name, hash=value["id"], select=value["select"],
                        active=True)
        await state.reset_state(TestStates.CHOICE_CARD_1[0])
        give_choice_card(open_cards=cards_right)


@dp.message_handler(state=TestStates.CHOICE_CARD_1[0])
async def process_callback_button1(callback_query: aiogram.types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = dp.current_state(user=user_id)
    get_card_info(int(user_id), callback_query.data)


executor = aiogram.executor.Executor(
    loop=asyncio.get_event_loop(),
    skip_updates=[],
    dispatcher=dp,
)
executor.start_polling()
