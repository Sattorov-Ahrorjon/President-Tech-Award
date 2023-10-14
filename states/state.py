from aiogram.dispatcher.filters.state import State, StatesGroup


class Lang(StatesGroup):
    lang = State()


class RegistrationKr(StatesGroup):
    name = State()
    phone_n = State()


class RegistrationRu(StatesGroup):
    name = State()
    phone_n = State()


class EmergencyKr(StatesGroup):
    situation = State()
    name = State()
    age = State()
    phone_n = State()
    location = State()


class EmergencyRu(StatesGroup):
    situation = State()
    name = State()
    age = State()
    phone_n = State()
    location = State()


class ConditionKr(StatesGroup):
    button = State()
    message = State()
    analysis = State()
    register = State()


class ConditionRu(StatesGroup):
    button = State()
    message = State()
    analysis = State()
    register = State()
