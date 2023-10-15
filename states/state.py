from aiogram.dispatcher.filters.state import State, StatesGroup


class Lang(StatesGroup):
    lang = State()


# class RegistrationKr(StatesGroup):
#     name = State()
#     phone_n = State()
#
#
# class RegistrationRu(StatesGroup):
#     name = State()
#     phone_n = State()


class EmergencyUz(StatesGroup):
    situation = State()
    emergency_name = State()
    age = State()
    phone_n = State()
    location = State()


class EmergencyRu(StatesGroup):
    situation = State()
    emergency_name = State()
    age = State()
    phone_n = State()
    location = State()


class ConditionUz(StatesGroup):
    type = State()
    message = State()
    analysis = State()
    condition_name = State()
    phone = State()


class ConditionRu(StatesGroup):
    type = State()
    message = State()
    analysis = State()
    name = State()
    phone = State()
