from aiogram.dispatcher.filters.state import State, StatesGroup


class Lang(StatesGroup):
    lang = State()


class RegistrationKr(StatesGroup):
    name = State()
    phone_n = State()


class RegistrationRu(StatesGroup):
    name = State()
    phone_n = State()


class UrgentHelpKr(StatesGroup):
    situation = State()
    name = State()
    phone_n = State()
    location = State()


class UrgentHelpRu(StatesGroup):
    situation = State()
    name = State()
    phone_n = State()
    location = State()
