import requests
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import DOMAIN, BOT_TOKEN, headers
from keyboards.default import def_buttons
from states.state import ConditionRu


def situation_list_func_ru():
    data_list = requests.get(
        url=f"{DOMAIN}/disease",
        # headers=headers
    ).json()

    return [v['name_disease'] for v in data_list]


@dp.message_handler(lambda message: message.text == "Подавать жалобу!")
async def download_image(message: types.Message):
    await message.answer(
        text="Выберите ситуацию, которую вы чувствуете в себе!",
        reply_markup=await def_buttons.condition_assessment_funk(lang='ru')
    )
    await ConditionRu.type.set()


@dp.message_handler(lambda message: message.text in situation_list_func_ru(), state=ConditionRu.type)
async def receiving_a_complaint(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text

    await message.answer(
        text="Предоставьте информацию о ситуации!"
             "\nВ текстовом виде!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await ConditionRu.message.set()


@dp.message_handler(state=ConditionRu.type)
async def receiving_a_complaint(message: types.Message):
    await message.answer(
        text="Пожалуйста!"
             "\nВыберите ситуацию, которую вы чувствуете в себе!",
        reply_markup=await def_buttons.condition_assessment_funk(lang='ru')
    )
    await ConditionRu.type.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=ConditionRu.message)
async def complaint_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    await message.answer(
        text="1) - savol."
             "\n2) - savol."
             "\nSavollarga javob bering!"
    )

    await ConditionRu.analysis.set()


@dp.message_handler(state=ConditionRu.analysis)
async def get_analysis(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['analysis'] = message.text

    await message.answer(
        text="Для вызова скорой помощи необходима базовая информация!!"
             "\nУкажите имя и фамилию пациента",
    )

    await ConditionRu.name.set()

# @dp.message_handler(content_types=types.ContentType.VOICE, state=ConditionRu.message)
# async def complaint_voice(message: types.Message, state: FSMContext):
#     voice_message = message.voice
#     file_id = voice_message.file_id
#     file_info = await bot.get_file(file_id=file_id)
#     file_path = file_info.file_path
#
#     download_link = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
#     await message.answer(
#         text=f"Javob qabul qilindi!"
#              f"\nRo'yxatdan o'tishingiz kerak"
#              f"\n{download_link}"
#     )
#
#     async with state.proxy() as data:
#         data['voice'] = download_link
#
#     await ConditionRu.name.set()
