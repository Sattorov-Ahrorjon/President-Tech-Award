import requests
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import X_API_KEY, DOMAIN
from keyboards.default import def_buttons

headers = {
    'X-API-KEY': X_API_KEY
}


def situation_list_func_ru():
    data_list = requests.get(
        url=f"{DOMAIN}/disease",
        # headers=headers
    ).json()

    return [v['name_disease'] for v in data_list]


@dp.message_handler(lambda message: message.text == "Подавать жалобу!")
async def download_image(message: types.Message, state: FSMContext):
    await message.answer(
        text="Выберите ситуацию, которую вы чувствуете в себе!",
        reply_markup=await def_buttons.condition_assessment_funk()
    )
