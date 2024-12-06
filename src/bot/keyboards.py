from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

basic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Команды', callback_data='help'), InlineKeyboardButton(text='О боте', callback_data='info')]
])

msk_ao = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ЦАО', callback_data='ao:ЦАО'), InlineKeyboardButton(text='САО', callback_data='ao:САО'), InlineKeyboardButton(text='ЮАО', callback_data='ao:ЮАО')],
    [InlineKeyboardButton(text='ЗАО', callback_data='ao:ЗАО'), InlineKeyboardButton(text='ВАО', callback_data='ao:ВАО'), InlineKeyboardButton(text='CЗАО', callback_data='ao:СЗАО')],
    [InlineKeyboardButton(text='СВАО', callback_data='ao:СВАО'), InlineKeyboardButton(text='ЮЗАО', callback_data='ao:ЮЗАО'), InlineKeyboardButton(text='ЮВАО', callback_data='ao:ЮВАО')],
    #  [InlineKeyboardButton(text='ЗелАО', callback_data='zelao'), InlineKeyboardButton(text='НАО', callback_data='nao'), InlineKeyboardButton(text='ТАО', callback_data='tao')]
])

yes_no_furn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='ynf:1'), InlineKeyboardButton(text='Нет', callback_data='ynf:0')]
])

yes_no_park = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='ynp:1'), InlineKeyboardButton(text='Нет', callback_data='ynp:0')]
])