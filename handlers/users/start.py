import requests
from loader import dp
from aiogram import types
from states.state import Lang
from keyboards.default import def_buttons
from aiogram.dispatcher import FSMContext
from data.config import X_API_KEY, DOMAIN
from keyboards.inline.inl_buttons import select_lang
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.exceptions import MessageToDeleteNotFound

headers = {
    'X-API-KEY': X_API_KEY
}


@dp.message_handler(commands=['state_stop'], state='*')
async def stop_state(message: types.Message, state: FSMContext):
    await message.answer(
        text="State stop!"
    )
    await state.finish()


@dp.message_handler(lambda message: message.text == "🏠 Бош саҳифа", state='*')
async def stop_state(message: types.Message, state: FSMContext):
    await message.answer(
        text="Сизга қандай ёрдам бера оламиз!",
        reply_markup=def_buttons.user_status_uz
    )
    await state.finish()


@dp.message_handler(lambda message: message.text == "🏠 Домашняя страница", state='*')
async def stop_state(message: types.Message, state: FSMContext):
    await message.answer(
        text="Как мы можем вам помочь!",
        reply_markup=def_buttons.user_status_ru
    )
    await state.finish()


# @dp.message_handler(CommandStart() test )
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    if requests.get(url=f"{DOMAIN}/user/{message.from_user.id}").json()['result']:

        if requests.get(url=f"{DOMAIN}/user/{message.from_user.id}").json()['user']['language'] == 'uz':
            await message.answer(
                text=f"Aссалому алайкум, {message.from_user.full_name}!"
                     f"\nСизга қандай ёрдам бера оламиз!",
                reply_markup=def_buttons.user_status_uz
            )
            return
        elif requests.get(url=f"{DOMAIN}/user/{message.from_user.id}").json()['user']['language'] == 'ru':
            await message.answer(
                text="\nЗдравствуйте, {message.from_user.full_name}!"
                     "Как мы можем вам помочь!",
                reply_markup=def_buttons.user_status_ru
            )
            return

    await message.answer(
        text=f"Aссалому алайкум, {message.from_user.full_name}!"
             f"\nЗдравствуйте, {message.from_user.full_name}!"
    )

    await message.answer(
        text="Тилни танланг!"
             "\nВыберите язык!",
        reply_markup=select_lang
    )
    await Lang.lang.set()


@dp.callback_query_handler(lambda call: bool(call.data == 'uz'), state=Lang.lang)
async def get_answer(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except MessageToDeleteNotFound:
        pass

    if not requests.get(url=f"{DOMAIN}/user/{call.from_user.id}").json()['result']:
        requests.post(
            url=f"{DOMAIN}/user/",
            data={
                'user_id': call.from_user.id,
                'language': 'uz'
            }
        )

    await call.message.answer(
        text="Сизга қандай ёрдам бера оламиз!",
        reply_markup=def_buttons.user_status_uz
    )
    await state.finish()


@dp.callback_query_handler(lambda call: bool(call.data == 'ru'), state=Lang.lang)
async def get_answer(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except MessageToDeleteNotFound:
        pass

    if not requests.get(url=f"{DOMAIN}/user/{call.from_user.id}").json()['result']:
        requests.post(
            url=f"{DOMAIN}/user/",
            data={
                'user_id': call.from_user.id,
                'language': 'ru'
            }
        )

    await call.message.answer(
        text="Как мы можем вам помочь!",
        reply_markup=def_buttons.user_status_ru
    )
    await state.finish()


@dp.callback_query_handler(state=Lang.lang)
async def get_answer(call: types.CallbackQuery):
    await call.message.answer(
        text="Тилни танланг!"
             "\nВыберите язык!",
        reply_markup=select_lang
    )
    await Lang.lang.set()


@dp.message_handler(state=Lang.lang)
async def get_answer(message: types.Message):
    await message.answer(
        text="Илтимос!"
             "\nТилни танланг!"
             "\nВыберите язык!",
        reply_markup=select_lang
    )
    await Lang.lang.set()
