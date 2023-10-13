from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    phone_n = State()
