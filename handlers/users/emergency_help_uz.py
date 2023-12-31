import requests
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.state import EmergencyUz
from keyboards.default import def_buttons
from data.config import X_API_KEY, DOMAIN

headers = {
    'X-API-KEY': X_API_KEY
}


def situation_list_func_kr():
    data_list = requests.get(
        url=f"{DOMAIN}/ttb",
        # headers=headers
    ).json()

    return [v['category'] for v in data_list]


@dp.message_handler(lambda message: message.text == "Тез ёрдам чақириш!")
async def know_the_situation(message: types.Message):
    await message.answer(
        text="Бемор ҳолати ҳақида малумот беринг!",
        reply_markup=await def_buttons.emergency_help_funk(lang='uz')
    )
    await EmergencyUz.situation.set()


@dp.message_handler(lambda message: message.text in situation_list_func_kr(), state=EmergencyUz.situation)
async def know_the_situation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['situation'] = message.text

    await message.answer(
        text="Тез тиббий ёрдам чақириш учун асосий малумотлар керак!"
             "\nБеморнинг исм фамилиясини юборинг",
        reply_markup=ReplyKeyboardRemove()
    )
    await EmergencyUz.emergency_name.set()


# lambda message: message.text not in situation_list_func_ru(),
@dp.message_handler(state=EmergencyUz.situation)
async def know_the_situation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['situation'] = message.text
    await message.answer(
        text="Илтимос!"
             "\nБемор ҳолати ҳақида малумот беринг!",
        reply_markup=await def_buttons.emergency_help_funk(lang='uz')
    )
    await EmergencyUz.situation.set()


@dp.message_handler(state=EmergencyUz.emergency_name)
async def patient_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text.capitalize()

    await message.answer(
        text="Беморнинг ёш оралиғини танланг!",
        reply_markup=def_buttons.user_age
    )
    await EmergencyUz.age.set()


@dp.message_handler(lambda message: message.text in ['0 - 6', '6 - 14', '14 - 18', '18 - *'], state=EmergencyUz.age)
async def get_user_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    message_ = "Тезкор алоқага чиқиш учун"
    message_ += "\n<strong>Рақамни юбориш</strong> тугмасини босинг"
    message_ += "\nЁки 901234567 кўринишида киритинг"

    await message.answer(
        text=message_,
        reply_markup=def_buttons.phone_number_uz
    )
    await EmergencyUz.phone_n.set()


@dp.message_handler(state=EmergencyUz.age)
async def get_user_age_error(message: types.Message):
    await message.answer(
        text="Илтимос!"
             "\nБеморнинг ёш оралиғини танланг!",
        reply_markup=def_buttons.user_age
    )
    await EmergencyUz.age.set()


@dp.message_handler(state=EmergencyUz.phone_n, content_types=types.ContentType.CONTACT)
async def patient_phone_contact(message: types.Message, state: FSMContext):
    phone_ = message.contact.phone_number
    if message.contact.phone_number.startswith('+'):
        phone_ = message.contact.phone_number[1:]

    async with state.proxy() as data:
        data['phone_n'] = phone_

    await message.answer(
        text=f"Жойлашув малумотини юбориш учун"
             f"\n<strong>Жойлашувни юбориш!</strong> тугмасини босинг",
        reply_markup=def_buttons.location_uz
    )
    await EmergencyUz.location.set()


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=EmergencyUz.phone_n)
async def patient_phone_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_n'] = "998" + message.text

    await message.answer(
        text=f"Жойлашув малумотини юбориш учун"
             f"\n<strong>Жойлашувни юбориш!</strong> тугмасини босинг",
        reply_markup=def_buttons.location_uz
    )
    await EmergencyUz.location.set()


@dp.message_handler(state=EmergencyUz.phone_n)
async def patient_phone_error(message: types.Message):
    message_ = "Илтимос! Тезкор алоқага чиқиш учун"
    message_ += "\n<strong>Рақамни юбориш</strong> тугмасини босинг"
    message_ += "\nЁки 901234567 кўринишида киритинг"
    await message.answer(text=message_, reply_markup=def_buttons.phone_number_uz)
    await EmergencyUz.phone_n.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=EmergencyUz.location)
async def patient_location_kr(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass

    requests.post(
        url=f"{DOMAIN}/history/",
        data={
            'user': message.from_user.id,
            'name': data['name'],
            'phone_number': data['phone_n'],
            'age': data['age'],
            'category': data['situation'],
            'latitude': message.location.latitude,
            'longitude': message.location.longitude,
        }
    )

    response = requests.get(
        url=f"{DOMAIN}/ttb/{data['situation']}"
    ).json()

    await message.answer(
        text=f"Малумотлар қабул қилинди!\n{data['situation']} бўйича биринчи ёрдам кўрсатиш йўриқномаси: http://168.119.110.233:5003/{response.get('image')}",
        reply_markup=def_buttons.user_status_uz
    )

    await state.finish()


@dp.message_handler(state=EmergencyUz.location)
async def patient_location_error(message: types.Message):
    await message.answer(
        text=f"Илтимос! Жойлашув малумотини юбориш учун"
             f"\n<strong>Жойлашувни юбориш!</strong> тугмасини босинг",
        reply_markup=def_buttons.location_uz
    )
    await EmergencyUz.location.set()
