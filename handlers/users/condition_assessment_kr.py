from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import X_API_KEY, DOMAIN
from keyboards.default import def_buttons

headers = {
    'X-API-KEY': X_API_KEY
}


@dp.message_handler(lambda message: message.text == "Шикоят билдириш!")
async def download_image(message: types.Message, state: FSMContext):
    await message.answer(
        text="Ўзингизда сезилаётган ҳолатни танланг!",
        reply_markup=await def_buttons.condition_assessment_funk()
    )

