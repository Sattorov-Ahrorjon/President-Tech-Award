from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

emergency_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bemorni holatini bilish!"),
        ],
        [
            KeyboardButton(text="Tez yordam!"),
        ],
    ],
    resize_keyboard=True
)

patient_conditions = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yurak xuruji"),
        ],
        [
            KeyboardButton(text="Jarohat olish holati")
        ],
        [
            KeyboardButton(text="Sinish holati")
        ]
    ],
    resize_keyboard=True
)

phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Raqamni yuborish!", request_contact=True),
        ]
    ],
    resize_keyboard=True
)

location = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Joylashuv malumoti!", request_location=True),
        ]
    ],
    resize_keyboard=True
)
