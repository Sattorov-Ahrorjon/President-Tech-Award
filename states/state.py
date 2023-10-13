from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    name = State()
    phone_n = State()


class UrgentHelp(StatesGroup):
    situation = State()
    name = State()
    phone_n = State()
    location = State()
