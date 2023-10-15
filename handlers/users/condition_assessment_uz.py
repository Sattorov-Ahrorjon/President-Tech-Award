import requests
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import DOMAIN, BOT_TOKEN, headers
from keyboards.default import def_buttons
from states.state import ConditionUz


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
    await ConditionUz.type.set()


@dp.message_handler(lambda message: message.text in situation_list_func_kr(), state=ConditionUz.type)
async def receiving_a_complaint(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text

    await message.answer(
        text="Ҳолат ҳақида малумот беринг!"
             "\nМатн кўринишида!",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await ConditionUz.message.set()


@dp.message_handler(state=ConditionUz.type)
async def receiving_a_complaint(message: types.Message):
    await message.answer(
        text="Илтимос!"
             "\nЎзингизда сезилаётган касаллик ҳолатини танланг!",
        reply_markup=await def_buttons.condition_assessment_funk()
    )
    await ConditionUz.type.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=ConditionUz.message)
async def complaint_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    await message.answer(
        text="1) - savol."
             "\n2) - savol."
             "\nSavollarga javob bering!"
    )

    await ConditionUz.analysis.set()


@dp.message_handler(state=ConditionUz.analysis)
async def get_analysis(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['analysis'] = message.text

    await message.answer(
        text="Тез тиббий ёрдам чақириш учун асосий малумотлар керак!"
             "\nБеморнинг исм фамилиясини юборинг"
    )
    await ConditionUz.condition_name.set()

# @dp.message_handler(content_types=types.ContentType.VOICE, state=ConditionKr.message)
# async def complaint_voice(message: types.Message, state: FSMContext):
#     voice_message = message.voice
#     file_id = voice_message.file_id
#     file_info = await bot.get_file(file_id=file_id)
#     file_path = file_info.file_path
#
#     download_link = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
#     await message.answer(
#         text=f"Javob qabul qilindi!"
#              f"\n{download_link}"
#              f"\nRo'yxatdan o'tish uchun \nIsm Familiyangizni kiriting"
#              "\nM-n: Sattorov Ahror"
#     )
#
#     async with state.proxy() as data:
#         data['voice'] = download_link
#
#     await ConditionKr.name.set()
