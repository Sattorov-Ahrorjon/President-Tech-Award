from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.state import UrgentHelpRu
from keyboards.default import def_buttons
from data.config import X_API_KEY, DOMAIN

headers = {
    'X-API-KEY': X_API_KEY
}


@dp.message_handler(lambda message: message.text == "Вызовите скорую!")
async def know_the_situation(message: types.Message):
    await message.answer(
        text="Предоставить информацию о состоянии пациента!",
        reply_markup=await def_buttons.emergency_help_funk()
    )
    await UrgentHelpRu.situation.set()


@dp.message_handler(lambda message: message.text in situation_list, state=UrgentHelpRu.situation)
async def know_the_situation(message: types.Message, state: FSMContext):
    await state.update_data({'situation': message.text})
    await message.answer(
        text="Для вызова скорой помощи необходима базовая информация!!"
             "\nУкажите имя и фамилию пациента"
    )
    await UrgentHelpRu.name.set()


@dp.message_handler(lambda message: message.text not in situation_list, state=UrgentHelpRu.situation)
async def know_the_situation(message: types.Message, state: FSMContext):
    await state.update_data({'situation': message.text})
    await message.answer(
        text="Пожалуйста!"
             "\nПредоставить информацию о состоянии пациента!",
        reply_markup=await def_buttons.emergency_help_funk()
    )
    await UrgentHelpRu.situation.set()


@dp.message_handler(state=UrgentHelpRu.name)
async def patient_name(message: types.Message, state: FSMContext):
    await state.update_data({'patient_name': message.text.capitalize()})
    message_ = "Для мгновенного контакта"
    message_ += "\nНажмите <strong>Отправить номер!</strong>"
    message_ += "\nИли введите его как 901234567"
    await message.answer(text=message_, reply_markup=def_buttons.phone_number_ru)
    await UrgentHelpRu.phone_n.set()


@dp.message_handler(state=UrgentHelpRu.phone_n, content_types=types.ContentType.CONTACT)
async def patient_phone_contact(message: types.Message, state: FSMContext):
    phone_ = message.contact.phone_number
    if message.contact.phone_number.startswith('+'):
        phone_ = message.contact.phone_number[1:]
    await state.update_data({'phone_n': phone_})

    await message.answer(
        text=f"Чтобы отправить информацию о местоположении"
             f"\nНажмите <strong>Отправить местоположение!</strong>",
        reply_markup=def_buttons.location_ru
    )
    await UrgentHelpRu.location.set()


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=UrgentHelpRu.phone_n)
async def patient_phone_text(message: types.Message, state: FSMContext):
    phone_n = "998" + message.text
    await state.update_data({'phone_n': phone_n})

    await message.answer(
        text=f"Чтобы отправить информацию о местоположении"
             f"\nНажмите <strong>Отправить местоположение!</strong>",
        reply_markup=def_buttons.location_ru
    )
    await UrgentHelpRu.location.set()


@dp.message_handler(state=UrgentHelpRu.phone_n)
async def patient_phone_error(message: types.Message):
    message_ = "Пожалуйста! Для мгновенного контакта"
    message_ += "\nНажмите <strong>Отправить номер</strong>"
    message_ += "\nИли введите его как 901234567"
    await message.answer(text=message_, reply_markup=def_buttons.phone_number_ru)
    await UrgentHelpRu.phone_n.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=UrgentHelpRu.location)
async def patient_location(message: types.Message, state: FSMContext):
    await message.answer(text="Alo")
    print(message.location)
    print(message.location.values)
    print(message.location.latitude)
    print(message.location.longitude)
    await state.finish()


@dp.message_handler(state=UrgentHelpRu.location)
async def patient_location_error(message: types.Message):
    await message.answer(
        text=f"Пожалуйста! Чтобы отправить информацию о местоположении"
             f"\nНажмите <strong>Отправить местоположение!</strong>",
        reply_markup=def_buttons.location_ru
    )
    await UrgentHelpRu.location.set()
