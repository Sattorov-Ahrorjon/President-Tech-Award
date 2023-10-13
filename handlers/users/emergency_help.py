from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.state import UrgentHelp
from keyboards.default.def_buttons import urgent_help, phone_number, location


@dp.message_handler(lambda message: message.text == "Tez yordam!")
async def know_the_situation(message: types.Message):
    await message.answer(
        text="Bemor holati haqida malumot bering!",
        reply_markup=await urgent_help()
    )
    await UrgentHelp.situation.set()


@dp.message_handler(state=UrgentHelp.situation)
async def know_the_situation(message: types.Message, state: FSMContext):
    await state.update_data({'situation': message.text})
    # Birinchi yordam malumotlari ulashiladi

    await message.answer(
        text="Tez tibbiy yordam chaqirish uchun asosiy malumotlar kerak!"
             "\nBemorning ism familiyasini yuboring"
    )
    await UrgentHelp.name.set()


@dp.message_handler(state=UrgentHelp.name)
async def patient_name(message: types.Message, state: FSMContext):
    await state.update_data({'patient_name': message.text.capitalize()})
    message_ = "Tezkor aloqaga chiqish uchun"
    message_ += "\n<strong>Raqamni yuborish</strong> tugmasini bosing"
    message_ += "\nYoki 901234567 ko'rinishida kiriting"
    await message.answer(text=message_, reply_markup=phone_number)
    await UrgentHelp.phone_n.set()


@dp.message_handler(state=UrgentHelp.phone_n, content_types=types.ContentType.CONTACT)
async def patient_phone_contact(message: types.Message, state: FSMContext):
    phone_ = None
    if message.contact.phone_number.startswith('+'):
        phone_ = message.contact.phone_number[1:]
    await state.update_data({'phone_n': phone_})

    await message.answer(
        text=f"\n<strong>Joylashuvni yuborish!</strong> tugmasini bosing"
             f"\nJoylashuv malumotini yuboring",
        reply_markup=location
    )
    await UrgentHelp.location.set()


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=UrgentHelp.phone_n)
async def patient_phone_text(message: types.Message, state: FSMContext):
    phone_n = "998" + message.text
    await state.update_data({'phone_n': phone_n})

    await message.answer(
        text=f"\n<strong>Joylashuvni yuborish!</strong> tugmasini bosing"
             f"\nJoylashuv malumotini yuboring",
        reply_markup=location
    )
    await UrgentHelp.location.set()


@dp.message_handler(state=UrgentHelp.phone_n)
async def patient_phone_error(message: types.Message):
    message_ = "Iltimos!"
    message_ += "\n<strong>Raqamni yuborish</strong> tugmasini bosing"
    message_ += "\nYoki 901234567 ko'rinishida kiriting"
    await message.answer(text=message_, reply_markup=phone_number)
    await UrgentHelp.phone_n.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=UrgentHelp.location)
async def patient_location(message: types.Message, state: FSMContext):
    await message.answer(text="Alo")
    print(message.location)
    print(message.location.values)
    print(message.location.latitude)
    print(message.location.longitude)


@dp.message_handler(state=UrgentHelp.location)
async def patient_location_error(message: types.Message):
    await message.answer(
        text=f"Iltimos!"
             f"\n<strong>Joylashuvni yuborish!</strong> tugmasini bosing"
             f"\nJoylashuv malumotini yuboring",
        reply_markup=location
    )
    await UrgentHelp.location.set()
