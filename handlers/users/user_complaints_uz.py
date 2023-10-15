import requests
from keyboards.inline.inl_buttons import web_buttons
from data.config import headers, DOMAIN
from aiogram import types
from loader import dp


@dp.message_handler(lambda message: message.text == "Шикоятларим!")
async def user_complaints(message: types.Message):
    response = requests.get(
        url=f"{DOMAIN}/historycomplain/{message.from_user.id}"
    ).json()
    for res in response:
        await message.answer(
            res['text'] + f"\nhttp://zerodev.uz/client/{res['url']}/{message.from_user.id}",
            reply_markup=web_buttons(list_=res, user_id=message.from_user.id)
        )

    await message.answer(
        text="Shikoyatlarim!"
    )
