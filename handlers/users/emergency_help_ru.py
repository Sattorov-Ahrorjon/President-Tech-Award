import requests
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.state import EmergencyRu
from keyboards.default import def_buttons
from data.config import X_API_KEY, DOMAIN

headers = {
    'X-API-KEY': X_API_KEY
}


def situation_list_func_ru():
    data_list = requests.get(
        url=f"{DOMAIN}/ttb",
        # headers=headers
    ).json()

    return [v['category'] for v in data_list]


@dp.message_handler(lambda message: message.text == "Вызовите скорую!")
async def know_the_situation(message: types.Message):
    await message.answer(
        text="Предоставить информацию о состоянии пациента!",
        reply_markup=await def_buttons.emergency_help_funk()
    )
    await EmergencyRu.situation.set()


@dp.message_handler(lambda message: message.text in situation_list_func_ru(), state=EmergencyRu.situation)
async def know_the_situation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['situation'] = message.text
    await message.answer(
        text="Для вызова скорой помощи необходима базовая информация!!"
             "\nУкажите имя и фамилию пациента",
        reply_markup=ReplyKeyboardRemove()
    )
    await EmergencyRu.name.set()


# lambda message: message.text not in situation_list_func_ru(),
@dp.message_handler(state=EmergencyRu.situation)
async def know_the_situation(message: types.Message):
    await message.answer(
        text="Пожалуйста!"
             "\nПредоставить информацию о состоянии пациента!",
        reply_markup=await def_buttons.emergency_help_funk()
    )
    await EmergencyRu.situation.set()


@dp.message_handler(state=EmergencyRu.name)
async def patient_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text.capitalize()

    await message.answer(
        text="Выберите возрастной диапазон пациента!",
        reply_markup=def_buttons.user_age
    )
    await EmergencyRu.age.set()


@dp.message_handler(lambda message: message.text in ['0 - 6', '6 - 14', '14 - 18', '18 - *'], state=EmergencyRu.age)
async def know_the_situation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    message_ = "Для мгновенного контакта"
    message_ += "\nНажмите <strong>Отправить номер!</strong>"
    message_ += "\nИли введите его как 901234567"
    await message.answer(
        text=message_,
        reply_markup=def_buttons.phone_number_ru)
    await EmergencyRu.phone_n.set()


@dp.message_handler(state=EmergencyRu.age)
async def patient_name(message: types.Message):
    await message.answer(
        text="Пожалуйста!"
             "\nВыберите возрастной диапазон пациента!",
        reply_markup=def_buttons.user_age
    )
    await EmergencyRu.age.set()


@dp.message_handler(state=EmergencyRu.phone_n, content_types=types.ContentType.CONTACT)
async def patient_phone_contact(message: types.Message, state: FSMContext):
    phone_ = message.contact.phone_number
    if message.contact.phone_number.startswith('+'):
        phone_ = message.contact.phone_number[1:]

    async with state.proxy() as data:
        data['phone_n'] = phone_

    await message.answer(
        text=f"Чтобы отправить информацию о местоположении"
             f"\nНажмите <strong>Отправить местоположение!</strong>",
        reply_markup=def_buttons.location_ru
    )
    await EmergencyRu.location.set()


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=EmergencyRu.phone_n)
async def patient_phone_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_n'] = "998" + message.text

    await message.answer(
        text=f"Чтобы отправить информацию о местоположении"
             f"\nНажмите <strong>Отправить местоположение!</strong>",
        reply_markup=def_buttons.location_ru
    )
    await EmergencyRu.location.set()


@dp.message_handler(state=EmergencyRu.phone_n)
async def patient_phone_error(message: types.Message):
    message_ = "Пожалуйста! Для мгновенного контакта"
    message_ += "\nНажмите <strong>Отправить номер</strong>"
    message_ += "\nИли введите его как 901234567"
    await message.answer(text=message_, reply_markup=def_buttons.phone_number_ru)
    await EmergencyRu.phone_n.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=EmergencyRu.location)
async def patient_location_ru(message: types.Message, state: FSMContext):
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

    await message.answer(
        text="Данные получены!",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.finish()


@dp.message_handler(state=EmergencyRu.location)
async def patient_location_error(message: types.Message):
    await message.answer(
        text=f"Пожалуйста! Чтобы отправить информацию о местоположении"
             f"\nНажмите <strong>Отправить местоположение!</strong>",
        reply_markup=def_buttons.location_ru
    )
    await EmergencyRu.location.set()
