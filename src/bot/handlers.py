from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery
from aiogram.types import Message

from config import config
import src.bot.keyboards as kb

router = Router()

available_commands = {
    '/start': 'Запуск бота',
    '/info': 'Что умеет этот бот?',
    '/help': 'Список доступных команд',
    '/run': 'Запуск модели',
    '/predict': 'Прогноз стоимости подходящего жилья',
}

info_text = (
    'С помощью бота вы можете узнать ожидаемую рыночную стоимость аренды жилья в Москве.\n'
    'Используйте /predict для прогноза цены на аренду жилья. По запросу бота поочередно вводите '
    'характеристики квартиры, которые у вас есть.\n'
    'Пользуйтесь подсказками бота, если не знаете, что выбрать, или характеристика для вас не важна. '
    'Такие данные будут заменены средними значениями.'
)


class InputForm(StatesGroup):
    floor = State()
    num_floors = State()
    area = State()
    living_area = State()  # ?
    kitchen_area = State()  # ?
    num_rooms = State()
    with_furniture = State()
    address = State()  # ?
    ao = State()
    metro = State()
    price_per_month = State()  # ?
    num_balcony = State()  # ?
    agent = State()  # ?
    num_cargo_elevators = State()  # ?
    num_elevators = State()  # ?
    parking = State()


def get_help_text():
    global available_commands
    answer_text = 'Доступные команды: \n'
    for cmd, description in available_commands.items():
        answer_text += cmd + ' - ' + description + '\n'
    return answer_text


# def is_integer(text):
#     while True:
#         try:
#             value = int(text)
#             return True
#         except ValueError:
#             return False


async def show_data(data):
    print(
        data['floor'],
        data['num_floors'],
        data['area'],
        data['living_area'],
        data['kitchen_area'],
        data['num_rooms'],
        data['with_furniture'],
        data['address'],
        data['ao'],
        data['metro'],
        data['price_per_month'],
        data['num_balcony'],
        data['agent'],
        data['num_cargo_elevators'],
        data['num_elevators'],
        data['parking'],
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.first_name}! Этот бот умеет предсказывать цену на аренду недвижимости.', reply_markup=kb.basic)
    await state.clear()


@router.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer(info_text)


@router.message(Command('run'))
async def cmd_run(message: Message):
    await message.answer('Обучение модели запущено. Пожалуйста, дождитесь ответа.')


@router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await message.answer(get_help_text())


@router.message(Command('predict'))
async def cmd_predict(message: Message, state: FSMContext):
    await message.answer('Вводите характеристики квартиры по запросу бота')
    await state.set_state(InputForm.ao)
    await message.answer('Выберите административный округ:', reply_markup=kb.msk_ao)


@router.message(InputForm.ao)
@router.callback_query(F.data.startswith('ao:'))
async def step1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await callback.message.edit_text('Административный округ: ' + choice)
    await state.update_data(ao=choice)
    await state.set_state(InputForm.metro)
    await callback.message.answer('Станция метро')


@router.message(InputForm.metro)
async def step2(message: Message, state: FSMContext):
    answer = message.text.lower().strip()
    await state.update_data(metro=answer)
    await state.set_state(InputForm.num_rooms)
    await message.answer('Сколько комнат в квартире?')


@router.message(InputForm.num_rooms)
async def step3(message: Message, state: FSMContext):
    # TODO: проверка?
    await state.update_data(num_rooms=message.text)
    await state.set_state(InputForm.with_furniture)
    await message.answer('Есть ли мебель в квартире?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.HAS_FURNITURE))


@router.message(InputForm.with_furniture)
@router.callback_query(F.data.contains(f'{config.FEATURES.HAS_FURNITURE}:'))
async def step4(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await state.update_data(with_furniture=choice)
    await state.set_state(InputForm.area)
    await callback.message.answer('Какова площадь квартиры? Введите только число')


@router.message(InputForm.area)
async def step5(message: Message, state: FSMContext):
    # проверка?
    await state.update_data(area=message.text)
    await state.set_state(InputForm.floor)
    await message.answer('На каком этаже квартира?')


@router.message(InputForm.floor)
async def step6(message: Message, state: FSMContext):
    # проверка?
    await state.update_data(floor=message.text)
    await state.set_state(InputForm.num_floors)
    await message.answer('Сколько этажей в доме?')


@router.message(InputForm.num_floors)
async def step7(message: Message, state: FSMContext):
    # проверка?
    await state.update_data(num_floors=message.text)
    await state.set_state(InputForm.num_floors)
    await message.answer('Нужен ли паркинг?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.NEED_PARKING))


@router.message(InputForm.parking)
@router.callback_query(F.data.contains(f'{config.FEATURES.NEED_PARKING}:'))
async def step8(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await state.update_data(parking=choice)
    data = await state.get_data()
    for key, value in data.items():
        print(key + ' : ' + value)
    await state.clear()

    # TODO: use bot.edit_message() instead
    await callback.message.answer('Цена аренды по вашим характеристикам: ...')


@router.callback_query()
async def callback_handler(callback: CallbackQuery):
    await callback.answer()

    if callback.data == 'help':
        await callback.message.answer(get_help_text())

    elif callback.data == 'info':
        await callback.message.answer(info_text)


@router.message(F.text)
async def some_text(message: Message):
    await message.answer('Я вас не понял. Попробуйте /help', reply_markup=kb.basic)
