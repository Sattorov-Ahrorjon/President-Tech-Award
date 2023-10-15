import requests
from loader import dp
from aiogram import types
from data.config import DOMAIN
from states.state import ConditionRu
from aiogram.dispatcher import FSMContext
from keyboards.default import def_buttons


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

    if not requests.get(url=f"{DOMAIN}/user/{message.from_user.id}").json()['user']['phone_number']:
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
        text=f"Ваша жалоба принята и передана специалисту. "
             f"Ответ эксперта вы можете увидеть в разделе «Мои жалобы».",
        reply_markup=def_buttons.user_status_ru
    )

    await state.finish()


@dp.message_handler(lambda message: message.text.isdigit() and len(message.text) == 9, state=ConditionRu.phone)
async def registration_contact_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = "998" + message.text

    if not requests.get(url=f"{DOMAIN}/user/{message.from_user.id}").json()['user']['phone_number']:
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
        text=f"Ваша жалоба принята и передана специалисту. "
             f"Ответ эксперта вы можете увидеть в разделе «Мои жалобы».",
        reply_markup=def_buttons.user_status_ru
    )


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
