import requests

from data.config import headers, DOMAIN
from aiogram import types
from loader import dp


@dp.message_handler(lambda message: message.text == "Мои жалобы!")
async def user_complaints(message: types.Message):
    res = requests.get(
        url=f"{DOMAIN}/historycomplain/{message.from_user.id}"
    )
    print(res.json())
    await message.answer(
        text="Shikoyatlarim!"
    )
