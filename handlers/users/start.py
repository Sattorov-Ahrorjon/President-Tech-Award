from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from states.state import Registration
from keyboards.default.def_buttons import phone_number
from loader import dp


# @dp.message_handler(CommandStart() test )
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    message_ = f"Assalomu alaykum, {message.from_user.full_name}!"
    message_ += "\nRo'yxatdan o'tish uchun \nIsm Familiyangizni kiriting"
    message_ += "\nM-n: Sattorov Ahror"
    await message.answer(text=message_)
    await Registration.name.set()


@dp.message_handler(lambda message: message.text.isalpha(), state=Registration.name)
async def registration_name(message: types.Message, state: FSMContext):
    await state.update_data({
        'id': message.from_user.id,
        'name': message.text,
        'username': message.from_user.username
    })
    message_ = "<strong>Raqamni yuborish</strong> tugmasini bosing"
    message_ += "\nYoki 901234567 ko'rinishida kiriting"
    await message.answer(text=message_, reply_markup=phone_number)
    await Registration.phone_n.set()


@dp.message_handler(state=Registration.name)
async def registration_name(message: types.Message):
    message_ = "Iltimos, ismingizni to'g'ri kiriting!"
    await message.answer(text=message_)
    await Registration.name.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Registration.phone_n)
async def registration_name(message: types.Message, state: FSMContext):
    phone_n = None
    if message.contact.phone_number.startswith('+'):
        phone_n = message.contact.phone_number[1:]
    await state.update_data({'phone_n': phone_n})
    message_ = f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!"
    # api request

    await message.answer(text=message_)
    await state.finish()


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=Registration.phone_n)
async def register_complete_handler(message: types.Message, state: FSMContext):
    phone_n = "998" + message.text
    await state.update_data({'phone_n': phone_n})
    message_ = f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!"
    # api request

    await message.answer(text=message_)
    await state.finish()


@dp.message_handler(state=Registration.phone_n)
async def registration_name(message: types.Message):
    message_ = "Iltimos!"
    message_ += "\n<strong>Raqamni yuborish</strong> tugmasini bosing"
    message_ += "\nYoki 901234567 ko'rinishida kiriting"
    await message.answer(text=message_, reply_markup=phone_number)
    await Registration.phone_n.set()
