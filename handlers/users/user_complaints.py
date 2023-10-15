from data.config import headers
from aiogram import types
from loader import dp


@dp.message_handler(lambda message: message.text == "Шикоятларим!")
async def user_complaints(message: types.Message):
    await message.answer(
        text="Shikoyatlarim!"
    )
