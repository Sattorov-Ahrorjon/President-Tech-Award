from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import requests
from data.config import X_API_KEY, DOMAIN

headers = {
    'X-API-KEY': X_API_KEY
}

select_lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ўзбек тили", callback_data='uz'),
            InlineKeyboardButton(text="русский язык", callback_data='ru'),
        ],
    ],
)

web_view = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Web view", web_app=WebAppInfo(url="https://www.bootdey.com/snippets/view/Chat-box#preview")),
        ]
    ],
)
