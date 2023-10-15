from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data.config import X_API_KEY, DOMAIN
import requests

headers = {
    'X-API-KEY': X_API_KEY
}


# Bemorning holatini aniqlash uchun dynamic buttons list muammoni eshitish
async def condition_assessment_funk(lang):
    condition_assessment_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    # data_list = {} name_disease
    data_list = requests.get(
        url=f'{DOMAIN}/disease',
        # headers=headers
    ).json()

    disease_list = [v['name_disease'] for v in data_list]
    buttons = [[KeyboardButton(text=condition)] for condition in disease_list]
    for obj in buttons:
        condition_assessment_buttons.keyboard.append(obj)

    if lang == 'ru':
        condition_assessment_buttons.keyboard.append(
            [
                KeyboardButton(text='🏠 Домашняя страница')
            ],
        )
    else:
        condition_assessment_buttons.keyboard.append(
            [
                KeyboardButton(text='🏠 Бош саҳифа')
            ],
        )

    return condition_assessment_buttons


async def emergency_help_funk(lang):
    urgent_help_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    data_list = {}
    data_list = requests.get(
        url=f"{DOMAIN}/ttb",
        # headers=headers
    ).json()

    emergency_help_list = [v['category'] for v in data_list]
    buttons = [[KeyboardButton(text=emergency_help)] for emergency_help in emergency_help_list]
    for obj in buttons:
        urgent_help_buttons.keyboard.append(obj)

    if lang == 'ru':
        urgent_help_buttons.keyboard.append(
            [
                KeyboardButton(text='🏠 Домашняя страница')
            ],
        )
    else:
        urgent_help_buttons.keyboard.append(
            [
                KeyboardButton(text='🏠 Бош саҳифа')
            ],
        )

    return urgent_help_buttons


phone_number_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Рақамни юбориш!", request_contact=True),
        ],
        [
            KeyboardButton(text='🏠 Бош саҳифа')
        ],
    ],
    resize_keyboard=True
)

phone_number_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить номер!", request_contact=True),
        ],
        [
            KeyboardButton(text='🏠 Домашняя страница')
        ],
    ],
    resize_keyboard=True
)

location_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Жойлашувни юбориш!", request_location=True),
        ],
        [
            KeyboardButton(text='🏠 Бош саҳифа')
        ],
    ],
    resize_keyboard=True
)

location_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить местоположение!", request_location=True),
        ],
        [
            KeyboardButton(text='🏠 Домашняя страница')
        ],
    ],
    resize_keyboard=True
)

user_status_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Шикоят билдириш!"),
            KeyboardButton(text="Тез ёрдам чақириш!")
        ],
        [
            KeyboardButton("Шикоятларим!")
        ],
        [
            KeyboardButton(text='🏠 Бош саҳифа')
        ],
    ],
    resize_keyboard=True
)

user_status_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подавать жалобу!"),
            KeyboardButton(text="Вызовите скорую!")
        ],
        [
            KeyboardButton(text='🏠 Домашняя страница')
        ],
    ],
    resize_keyboard=True
)

user_age = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="0 - 6"),
            KeyboardButton(text="6 - 14")
        ],
        [
            KeyboardButton(text="14 - 18"),
            KeyboardButton(text="18 - *")
        ]
    ],
    resize_keyboard=True
)
