import asyncio
import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
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
    cookies="0E8FFE6C3B71611AF60A38FF71D2E4ED4ECAF447A0B45319F760AAF0AC511D32E482213B904961E1606841E81C73B8FF3BA22962F22A55EF5BBE56EA92306720F0EE5808E573B681E3C5FD6A20E6DBF6C25B4F1585DAF63A5D015CEAE79DA5881FB40823882033D92F354713F482707361E4C0FB27965036079B9586916F864B522F28FC0E528A80289C3D907AD95F19B3E87FD61977AA175917F3BAE3961922FF768CCD8F2F4966A5AF4DC8F5EEB3D005EC2DF40D06C8413241F8B563DD39B487C3AD0F3C577440FBB4445765EE13DDF7CCA525268506CC7AC4637D8B4CEDDB79BE1E7287BCCE7EB4D0F93BEDAE586FEEC2EB9314967CDDAB80BDB2B4D3D59AD02BF1918B4360D335005F62194D374533A40486553BAE8EABF1DFB4D77566F6638886EB"
)

if waildberries_b:
    print("Start py_yg")
    logger.info("Py_tg working.")


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
    await bot.answer_callback_query(callback_query.id)
    if callback_data[0] == 'buy':
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
        await state.set_state(TestStates.CHOICE_CARD_1[0])
        await give_choice_card(open_cards=cards_right)


@dp.callback_query_handler(state=TestStates.CHOICE_CARD_1[0])
async def process_callback_button1(callback_query: aiogram.types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    logger.info("Prepare after buying")
    user_id = callback_query.from_user.id
    state = dp.current_state(user=user_id)
    data = callback_query.data.split('.')
    if data[1] == '1':
        card = get_card_info(int(user_id), data[0])
        waildberries_b.payment_by_card(card)
    else:
        card = get_card_info(int(user_id), data[0])
        flag = waildberries_b.choosing_a_bank_card(card)
        if flag:
            if waildberries_b.payment_by_card(card):
                await bot.send_message(callback_query.from_user.id, "All good")
            else:
                await bot.send_message(callback_query.from_user.id, "Some problem")
            all_cards = get_active_cards(int(user_id))
            for card in all_cards:
                number = list(card.keys())[0]
                if number == data[0]:
                    update_card(int(user_id), number, select=True)
                else:
                    update_card(int(user_id), number, select=False)
    await state.reset_state()


executor = aiogram.executor.Executor(
    loop=asyncio.get_event_loop(),
    skip_updates=[],
    dispatcher=dp,
)
executor.start_polling()
