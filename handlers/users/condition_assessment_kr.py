import requests
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import X_API_KEY, DOMAIN, BOT_TOKEN
from keyboards.default import def_buttons
from states.state import ConditionKr, RegistrationKr

headers = {
    'X-API-KEY': X_API_KEY
}


def situation_list_func_kr():
    data_list = requests.get(
        url=f"{DOMAIN}/disease",
        # headers=headers
    ).json()

    return [v['name_disease'] for v in data_list]


@dp.message_handler(lambda message: message.text == "Шикоят билдириш!")
async def download_image(message: types.Message):
    await message.answer(
        text="Ўзингизда сезилаётган касаллик ҳолатини танланг!",
        reply_markup=await def_buttons.condition_assessment_funk()
    )
    await ConditionKr.button.set()


@dp.message_handler(lambda message: message.text in situation_list_func_kr(), state=ConditionKr.button)
async def receiving_a_complaint(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_disease'] = message.text

    await message.answer(
        text="Ҳолат ҳақида малумот беринг!"
             "\n Ovozli yoki matn ko'rinishida!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await ConditionKr.message.set()


@dp.message_handler(state=ConditionKr.button)
async def receiving_a_complaint(message: types.Message):
    await message.answer(
        text="Илтимос!"
             "\nЎзингизда сезилаётган касаллик ҳолатини танланг!",
        reply_markup=await def_buttons.condition_assessment_funk()
    )
    await ConditionKr.button.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=ConditionKr.message)
async def complaint_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    await message.answer(
        text="Javob qabul qilindi!"
    )
    await RegistrationKr.name.set()


@dp.message_handler(content_types=types.ContentType.VOICE, state=ConditionKr.message)
async def complaint_voice(message: types.Message, state: FSMContext):
    voice_message = message.voice
    file_id = voice_message.file_id
    file_info = await bot.get_file(file_id=file_id)
    file_path = file_info.file_path

    download_link = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
    await message.answer(
        text=f"Javob qabul qilindi!"
             f"\n{download_link}"
    )

    async with state.proxy() as data:
        data['voice'] = download_link

    await RegistrationKr.name.set()
