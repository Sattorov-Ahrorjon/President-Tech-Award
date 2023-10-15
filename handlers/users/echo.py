from aiogram import types
from loader import dp
# from aiogram.dispatcher.filters.builtin import CommandStart


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)

#
# @dp.message_handler(CommandStart())
# async def bot_echo(message: types.Message):
#     await message.answer(message.text, reply_markup=web_view)
