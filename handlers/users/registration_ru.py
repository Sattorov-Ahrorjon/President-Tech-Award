import requests
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.state import ConditionRu
from keyboards.default import def_buttons
from data.config import DOMAIN

@dp.message_handler(state=ConditionRu.name)
async def bot_start(message: types.Message, state: FSMContext):
    message_ = "Для мгновенного контакта"
    message_ += "\nНажмите <strong>Отправить номер!</strong>"
    message_ += "\nИли введите его как 901234567"
    await message.answer(
        text=message_,
        reply_markup=def_buttons.phone_number_uz
    )

    async with state.proxy() as data:
        data['name'] = message.text

    await ConditionRu.phone.set()


@dp.message_handler(state=ConditionRu.phone, content_types=types.ContentType.CONTACT)
async def registration_contact(message: types.Message, state: FSMContext):
    phone_ = message.contact.phone_number
    if message.contact.phone_number.startswith('+'):
        phone_ = message.contact.phone_number[1:]

    async with state.proxy() as data:
        data['phone'] = phone_

    # data_dic = {
    #     'name': data['name'],
    #     'phone': data['phone'],
    #     'type': data['type'],
    #     'text': data['text'],
    #     'analysis': data['analysis'],
    # }

    requests.put(
        url=f"{DOMAIN}/user/{message.from_user.id}/",
        json={
            'name': data['name'],
            'username': message.from_user.username,
            'phone_number': data['phone']
        }
    )

    requests.post(
        url=f"{DOMAIN}/complain/",
        json={
            'user': message.from_user.id,
            'category': data['type']
        }
    )

    await message.answer(
        text=f"Tugadi!\n",
        reply_markup=ReplyKeyboardRemove()
    )

    await state.finish()


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=ConditionRu.phone)
async def registration_contact_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = "998" + message.text

    # data_dic = {
    #     'name': data['name'],
    #     'phone': data['phone'],
    #     'type': data['type'],
    #     'text': data['text'],
    #     'analysis': data['analysis'],
    # }

    if not requests.get(url=f"{DOMAIN}/user/{message.from_user.id}").json()['result']:
        requests.put(
            url=f"{DOMAIN}/user/{message.from_user.id}/",
            json={
                'name': data['name'],
                'username': message.from_user.username,
                'phone_number': data['phone']
            }
        )

    requests.post(
        url=f"{DOMAIN}/complain/",
        json={
            'user': message.from_user.id,
            'category': data['type']
        }
    )

    await message.answer(
        text=f"Tugadi!\n",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.finish()


@dp.message_handler(state=ConditionRu.phone)
async def registration_contact_error(message: types.Message):
    message_ = "Пожалуйста!"
    message_ += "Для мгновенного контакта"
    message_ += "\nНажмите <strong>Отправить номер!</strong>"
    message_ += "\nИли введите его как 901234567"
    await message.answer(
        text=message_,
        reply_markup=def_buttons.phone_number_uz)
    await ConditionRu.phone.set()
