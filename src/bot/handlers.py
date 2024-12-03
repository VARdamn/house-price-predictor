from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

import src.bot.keyboards as keyboards

router = Router()

available_commands = {
    '/start' : 'запуск бота',
    '/info' : 'что умеет этот бот',
    '/help' : 'доступные команды',
    '/run' : 'запуск модели',
    '/predict' : 'прогноз цены'
}

def get_help_text():
    global available_commands
    answer_text = 'Доступные команды: \n'
    for cmd, descpription in available_commands.items():
        answer_text += cmd + ' - ' + descpription + '\n'
    return answer_text

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Этот бот умеет предсказывать цену на аренду недвижимости.',
                            reply_markup=keyboards.basic)

@router.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer('Здесь будет выведена информация о боте')

@router.message(Command('run'))
async def cmd_run(message: Message):
    await message.answer('Обучение модели запущено. Пожалуйста, дождитесь ответа.')

@router.message(Command('predict'))
async def cmd_predict(message: Message):
    await message.answer('Выберите административный округ Москвы: ', reply_markup=keyboards.msk_ao)

@router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await message.answer(get_help_text())

@router.message(F.text)
async def some_text(message: Message):
    await message.answer('Я вас не понял. Попробуйте /help', reply_markup=keyboards.basic)

@router.callback_query()
async def callback_handler(callback: CallbackQuery):
    await callback.answer()

    if callback.data == 'help':
        await callback.message.answer(get_help_text())

    elif callback.data == 'info':
        await callback.message.answer('Здесь будет выведена информация о боте')

@router.callback_query(F.data == 'tsao')
async def request_for_tsao(callback: CallbackQuery):
    print('test')



