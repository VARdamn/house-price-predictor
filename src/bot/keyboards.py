from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

basic = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Команды', callback_data='help'), InlineKeyboardButton(text='О боте', callback_data='info')]]
)

msk_districts = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='ЦАО', callback_data='district:ЦАО'),
            InlineKeyboardButton(text='САО', callback_data='district:САО'),
            InlineKeyboardButton(text='ЗАО', callback_data='district:ЗАО'),
        ],
        [
            InlineKeyboardButton(text='НАО (Новомосковский)', callback_data='district:НАО (Новомосковский)'),
            InlineKeyboardButton(text='Другой', callback_data='district:other'),
        ],
    ]
)


def parking_type() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Наземный', callback_data='parking_type:ground:наземный'),
                InlineKeyboardButton(text='Подземный', callback_data='parking_type:underground:подземный'),
                InlineKeyboardButton(text='Неважно', callback_data='parking_type:ground:неважно'),
            ]
        ]
    )


def lifts_count() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='1', callback_data='lifts_count:1'), InlineKeyboardButton(text='2', callback_data='lifts_count:2')],
            [InlineKeyboardButton(text='3', callback_data='lifts_count:3'), InlineKeyboardButton(text='4+', callback_data='lifts_count:4+')],
        ]
    )


def boolean_keyboard(feature: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да', callback_data=f'{feature}:1'),
                InlineKeyboardButton(text='Нет', callback_data=f'{feature}:0'),
            ]
        ]
    )
