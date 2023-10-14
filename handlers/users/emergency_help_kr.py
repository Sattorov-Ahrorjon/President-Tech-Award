from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.state import UrgentHelpKr, UrgentHelpRu
from keyboards.default import def_buttons
from data.config import X_API_KEY, DOMAIN

headers = {
    'X-API-KEY': X_API_KEY
}


@dp.message_handler(lambda message: message.text == "Тез ёрдам чақириш!")
async def know_the_situation(message: types.Message):
    await message.answer(
        text="Бемор ҳолати ҳақида малумот беринг!",
        reply_markup=await def_buttons.emergency_help_funk()
    )
    await UrgentHelpKr.situation.set()


@dp.message_handler(lambda message: message.text in situation_list, state=UrgentHelpKr.situation)
async def know_the_situation(message: types.Message, state: FSMContext):
    await state.update_data({'situation': message.text})
    await message.answer(
        text="Тез тиббий ёрдам чақириш учун асосий малумотлар керак!"
             "\nБеморнинг исм фамилиясини юборинг"
    )
    await UrgentHelpKr.name.set()


@dp.message_handler(lambda message: message.text not in situation_list, state=UrgentHelpKr.situation)
async def know_the_situation(message: types.Message, state: FSMContext):
    await state.update_data({'situation': message.text})
    await message.answer(
        text="Илтимос!"
             "\nБемор ҳолати ҳақида малумот беринг!",
        reply_markup=await def_buttons.emergency_help_funk()
    )
    await UrgentHelpKr.situation.set()


@dp.message_handler(state=UrgentHelpKr.name)
async def patient_name(message: types.Message, state: FSMContext):
    await state.update_data({'patient_name': message.text.capitalize()})
    message_ = "Тезкор алоқага чиқиш учун"
    message_ += "\n<strong>Рақамни юбориш</strong> тугмасини босинг"
    message_ += "\nЁки 901234567 кўринишида киритинг"
    await message.answer(text=message_, reply_markup=def_buttons.phone_number_kr)
    await UrgentHelpKr.phone_n.set()


@dp.message_handler(state=UrgentHelpKr.phone_n, content_types=types.ContentType.CONTACT)
async def patient_phone_contact(message: types.Message, state: FSMContext):
    phone_ = message.contact.phone_number
    if message.contact.phone_number.startswith('+'):
        phone_ = message.contact.phone_number[1:]
    await state.update_data({'phone_n': phone_})

    await message.answer(
        text=f"Жойлашув малумотини юбориш учун"
             f"\n<strong>Жойлашувни юбориш!</strong> тугмасини босинг",
        reply_markup=def_buttons.location_kr
    )
    await UrgentHelpKr.location.set()


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=UrgentHelpKr.phone_n)
async def patient_phone_text(message: types.Message, state: FSMContext):
    phone_n = "998" + message.text
    await state.update_data({'phone_n': phone_n})

    await message.answer(
        text=f"Жойлашув малумотини юбориш учун"
             f"\n<strong>Жойлашувни юбориш!</strong> тугмасини босинг",
        reply_markup=def_buttons.location_kr
    )
    await UrgentHelpKr.location.set()


@dp.message_handler(state=UrgentHelpKr.phone_n)
async def patient_phone_error(message: types.Message):
    message_ = "Илтимос! Тезкор алоқага чиқиш учун"
    message_ += "\n<strong>Рақамни юбориш</strong> тугмасини босинг"
    message_ += "\nЁки 901234567 кўринишида киритинг"
    await message.answer(text=message_, reply_markup=def_buttons.phone_number_kr)
    await UrgentHelpKr.phone_n.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=UrgentHelpKr.location)
async def patient_location(message: types.Message, state: FSMContext):
    await message.answer(text="Alo")
    print(message.location)
    print(message.location.values)
    print(message.location.latitude)
    print(message.location.longitude)
    await state.finish()

@dp.message_handler(state=UrgentHelpKr.location)
async def patient_location_error(message: types.Message):
    await message.answer(
        text=f"Илтимос! Жойлашув малумотини юбориш учун"
             f"\n<strong>Жойлашувни юбориш!</strong> тугмасини босинг",
        reply_markup=def_buttons.location_kr
    )
    await UrgentHelpKr.location.set()
