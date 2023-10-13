from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(lambda message: message.text == "Boshqa holat...")
async def download_image(message: types.Message, state: FSMContext):
    pass
