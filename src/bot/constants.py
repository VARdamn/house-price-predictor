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

district_map = {'ЦАО': 'ЦАО', 'САО': 'САО', 'ЗАО': 'ЗАО', 'НАО (Новомосковский)': 'НАО (Новомосковский)', 'other': 'ЮЗАО/ЮАО/ЮВАО/ВАО/СВАО/СЗАО'}

parking_type_map = {'ground': 'Наземная', 'underground': 'Подземная'}


def get_prediction_message(data, price):
    return f"""
Ваша квартира мечты:

🏠 Округ: <b>{district_map[data['district']]}</b>
🚇 Ближайшее метро: <b>{data['nearest_underground']} минут</b>
🛏️ Количество комнат: <b>{data['rooms_count']}</b>
🛋️ Мебель: <b>{'Есть' if data['has_furniture'] == 1 else 'Нет'}</b>
📏 Общая площадь: <b>{data['area']} м²</b>
🛋️ Жилая площадь: <b>{data['living_area']} м²</b>
🍽️ Площадь кухни: <b>{data['kitchen_area']} м²</b>
🏢 Этажность дома: <b>{data['floors_count']} этажей</b>
⬆️ Этаж вашей квартиры: <b>{data['floor']}</b>
🚗 Тип парковки: <b>{parking_type_map[data['parking_type']]}</b>
🌇 Балкон: <b>{'Есть' if data['has_balconies'] == 1 else 'Нет'}</b>
🛗 Количество лифтов: <b>{data['lifts_count']}</b>
📦 Грузовой лифт: <b>{'Есть' if data['has_cargo_lifts'] == 1 else 'Нет'}</b>
👨‍💼 Продавец — агент: <b>{'Да' if data['is_seller_agent'] == 1 else 'Нет'}</b>

💰 Ориентировочная стоимость: <b>{price} рублей</b>
"""


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
