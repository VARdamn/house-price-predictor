info_text = (
    'С помощью бота вы можете узнать ожидаемую рыночную стоимость аренды жилья в Москве.\n'
    'Используйте /predict для прогноза цены на аренду жилья. По запросу бота поочередно вводите '
    'характеристики квартиры, которые у вас есть.\n'
    'Пользуйтесь подсказками бота, если не знаете, что выбрать, или характеристика для вас не важна. '
    'Такие данные будут заменены средними значениями.'
)

available_commands = {
    '/start': 'Запуск бота',
    '/info': 'Что умеет этот бот?',
    '/help': 'Список доступных команд',
    '/predict': 'Прогноз стоимости подходящего жилья',
}


def get_help_text():
    global available_commands
    answer_text = 'Доступные команды: \n'
    for cmd, description in available_commands.items():
        answer_text += cmd + ' - ' + description + '\n'
    return answer_text


def is_integer(text):
    while True:
        try:
            value = int(text)
            return True
        except ValueError:
            return False
