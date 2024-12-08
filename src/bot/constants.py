info_message = (
    'С помощью бота вы можете узнать ожидаемую рыночную стоимость аренды жилья в Москве.\n\n'
    'Используйте /predict для прогноза цены на аренду жилья. По запросу бота поочередно вводите '
    'характеристики квартиры, которые у вас есть.\n\n'
    'Пользуйтесь подсказками бота, если не знаете, что выбрать, или характеристика для вас не важна. '
    'Такие данные будут заменены средними значениями.'
)

misunderstand_message = 'Я вас не понял. Попробуйте /help'

available_commands = {
    '/start': 'Запуск бота',
    '/info': 'Что умеет этот бот?',
    '/help': 'Список доступных команд',
    '/predict': 'Прогноз стоимости подходящего жилья',
}

bool_map = {
    '0': 'Нет',
    '1': 'Да',
}


def boolean_map(key: str) -> str:
    return bool_map.get(key) or 'Неважно'


def get_start_message(user_name: str) -> str:
    return f'Привет, {user_name}! Этот бот умеет предсказывать цену на аренду недвижимости.'


def get_help_message() -> str:
    global available_commands
    answer_text = 'Доступные команды: \n'
    for cmd, description in available_commands.items():
        answer_text += cmd + ' - ' + description + '\n'
    return answer_text


def is_integer(text: str) -> bool:
    return text.isdecimal()
