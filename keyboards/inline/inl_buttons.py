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


def web_buttons(list_, user_id):
    web_view = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    # text=f"{list_['text']}",
                    text="web - view",
                    web_app=WebAppInfo(url=f"https://zerodev.uz/client/{list_['url']}/{user_id}")),
                # web_app=WebAppInfo(url=f"https://168.119.110.233:5003/api/v1/messages/8/"), )
            ]
        ],
    )

    return web_view
