from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def patient_conditions():
    patient_conditions_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    data_list = {}
    # data_list = requests.get(
    #     url=f'',
    #     headers=headers
    # ).json()

    conditions = [v['key'] for v in data_list]
    buttons = [[KeyboardButton(text=condition)] for condition in conditions]
    for obj in buttons:
        patient_conditions_buttons.keyboard.append(obj)

    patient_conditions_buttons.keyboard.append(
        [
            KeyboardButton(text='Boshqa holat...')
        ],
    )

    return patient_conditions_buttons


#
# patient_conditions = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Yurak xuruji"),
#         ],
#         [
#             KeyboardButton(text="Jarohat olish holati")
#         ],
#         [
#             KeyboardButton(text="Sinish holati")
#         ]
#     ],
#     resize_keyboard=True
# )


async def urgent_help():
    urgent_help_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    data_list = {}
    # data_list = requests.get(
    #     url=f'',
    #     headers=headers
    # ).json()

    emergency_help_list = [v['key'] for v in data_list]
    buttons = [[KeyboardButton(text=emergency_help)] for emergency_help in emergency_help_list]
    for obj in buttons:
        urgent_help_buttons.keyboard.append(obj)

    urgent_help_buttons.keyboard.append(
        [
            KeyboardButton(text='Boshqa holat...')
        ],
    )

    return urgent_help_buttons


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
            KeyboardButton(text="Joylashuvni yuborish!", request_location=True),
        ]
    ],
    resize_keyboard=True
)

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
