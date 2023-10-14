from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from states.state import RegistrationKr, RegistrationRu, Lang
from keyboards.default import def_buttons
from keyboards.inline.inl_buttons import select_lang
from loader import dp
from data.config import X_API_KEY, DOMAIN
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


# @dp.message_handler(CommandStart() test )
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
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


@dp.callback_query_handler(lambda call: bool(call.data == 'kr'), state=Lang.lang)
async def get_answer(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except MessageToDeleteNotFound:
        pass
    await call.message.answer(
        text="Сизга қандай ёрдам бера оламиз!",
        reply_markup=def_buttons.user_status_kr
    )
    await state.finish()


@dp.callback_query_handler(lambda call: bool(call.data == 'ru'), state=Lang.lang)
async def get_answer(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
    except MessageToDeleteNotFound:
        pass
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

# @dp.message_handler(lambda message: message, state=Registration.lang)
# async def bot_start(message: types.Message):
#     message_ = f"Aссалому алайкум, {message.from_user.full_name}!"
#     message_ += "\nRo'yxatdan o'tish uchun \nIsm Familiyangizni kiriting"
#     message_ += "\nM-n: Sattorov Ahror"
#     await message.answer(text=message_)
#     await Registration.name.set()
#
#
# @dp.message_handler(lambda message: message.text.isalpha(), state=Registration.name)
# async def registration_name(message: types.Message, state: FSMContext):
#     await state.update_data({
#         'id': message.from_user.id,
#         'name': message.text,
#         'username': message.from_user.username
#     })
#     message_ = "<strong>Raqamni yuborish</strong> tugmasini bosing"
#     message_ += "\nYoki 901234567 ko'rinishida kiriting"
#     await message.answer(text=message_, reply_markup=phone_number)
#     await Registration.phone_n.set()
#
#
# @dp.message_handler(state=Registration.name)
# async def registration_name_error(message: types.Message):
#     message_ = "Iltimos, ismingizni to'g'ri kiriting!"
#     await message.answer(text=message_)
#     await Registration.name.set()
#
#
# @dp.message_handler(content_types=types.ContentType.CONTACT, state=Registration.phone_n)
# async def registration_phone_contact(message: types.Message, state: FSMContext):
#     phone_n = None
#     if message.contact.phone_number.startswith('+'):
#         phone_n = message.contact.phone_number[1:]
#     await state.update_data({'phone_n': phone_n})
#     message_ = f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!"
#     # api request
#
#     await message.answer(text=message_)
#     await state.finish()
#
#
# @dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=Registration.phone_n)
# async def registration_phone_text(message: types.Message, state: FSMContext):
#     phone_n = "998" + message.text
#     await state.update_data({'phone_n': phone_n})
#     message_ = f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!"
#     # api request ()
#
#     await message.answer(text=message_)
#     await state.finish()
#
#
# @dp.message_handler(state=Registration.phone_n)
# async def registration_phone_error(message: types.Message):
#     message_ = "Iltimos!"
#     message_ += "\n<strong>Raqamni yuborish</strong> tugmasini bosing"
#     message_ += "\nYoki 901234567 ko'rinishida kiriting"
#     await message.answer(text=message_, reply_markup=phone_number)
#     await Registration.phone_n.set()
