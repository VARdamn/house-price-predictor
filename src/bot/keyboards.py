from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

basic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Команды', callback_data='help'), InlineKeyboardButton(text='О боте', callback_data='info')]
])

msk_ao = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ЦАО', callback_data='ao:tsao'), InlineKeyboardButton(text='САО', callback_data='sao'), InlineKeyboardButton(text='ЮАО', callback_data='yuao')],
    [InlineKeyboardButton(text='ЗАО', callback_data='zao'), InlineKeyboardButton(text='ВАО', callback_data='vao'), InlineKeyboardButton(text='CЗАО', callback_data='szao')],
    [InlineKeyboardButton(text='СВАО', callback_data='svao'), InlineKeyboardButton(text='ЮЗАО', callback_data='yuzao'), InlineKeyboardButton(text='ЮВАО', callback_data='yuvao')],
    #  [InlineKeyboardButton(text='ЗелАО', callback_data='zelao'), InlineKeyboardButton(text='НАО', callback_data='nao'), InlineKeyboardButton(text='ТАО', callback_data='tao')]
])