from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from config import config
from src.bot.constants import get_help_text, info_text, is_integer
from src.bot.states import InputForm
import src.bot.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.first_name}! Этот бот умеет предсказывать цену на аренду недвижимости.', reply_markup=kb.basic)
    await state.clear()


@router.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer(info_text)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(get_help_text())


@router.message(Command('predict'))
async def cmd_predict(message: Message, state: FSMContext):
    await message.answer('Вводите характеристики квартиры по запросу бота')
    await state.set_state(InputForm.ao)
    await message.answer('Выберите административный округ:', reply_markup=kb.msk_ao)


@router.callback_query(F.data.startswith('ao:'), InputForm.ao)
async def step1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await callback.message.edit_text('Административный округ: ' + f'<i>{choice}</i>')
    await state.update_data(ao=choice)
    await state.set_state(InputForm.metro)
    await callback.message.answer('Сколько минут идти до метро?')


@router.message(InputForm.metro)
async def step2(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(metro=message.text)
    await state.set_state(InputForm.num_rooms)
    await message.answer('Сколько комнат в квартире?')


@router.message(InputForm.num_rooms)
async def step3(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(num_rooms=message.text)
    await state.set_state(InputForm.with_furniture)
    await message.answer('Есть ли мебель в квартире?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.HAS_FURNITURE))


@router.callback_query(F.data.contains(f'{config.FEATURES.HAS_FURNITURE}:'), InputForm.with_furniture)
async def step4(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    if choice == '1':
        await callback.message.edit_text('Мебель: <i>Да</i>')
    elif choice == '0':
        await callback.message.edit_text('Мебель: <i>Нет</i>')
    else:
        await callback.message.edit_text('Мебель: <i>Не важно</i>')
    await state.update_data(with_furniture=choice)
    await state.set_state(InputForm.area)
    await callback.message.answer('Какова площадь квартиры?')


@router.message(InputForm.area)
async def step5(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(area=message.text)
    await state.set_state(InputForm.floor)
    await message.answer('На каком этаже квартира?', reply_markup=kb.not_important_btn(config.FEATURES.FLOOR))


@router.callback_query(F.data.contains(f'{config.FEATURES.FLOOR}:'), InputForm.floor)
async def step6(callback : CallbackQuery, state: FSMContext):
    await state.update_data(floor='None')
    await callback.message.edit_text('Этаж: <i>Не важно</i>')
    await state.set_state(InputForm.num_floors)
    await callback.message.answer('Сколько этажей в доме?', reply_markup=kb.not_important_btn(config.FEATURES.NUM_FLOORS))


@router.message(InputForm.floor)
async def step6(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(floor=message.text)
    await state.set_state(InputForm.num_floors)
    await message.answer('Сколько этажей в доме?', reply_markup=kb.not_important_btn(config.FEATURES.NUM_FLOORS))


@router.callback_query(F.data.contains(f'{config.FEATURES.NUM_FLOORS}:'), InputForm.num_floors)
async def step7(callback : CallbackQuery, state: FSMContext):
    await state.update_data(num_floors='None')
    await callback.message.edit_text('Количество этажей: <i>Не важно</i>')
    await state.set_state(InputForm.parking)
    await callback.message.answer('Нужен ли паркинг?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.NEED_PARKING))


@router.message(InputForm.num_floors)
async def step7(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(num_floors=message.text)
    await state.set_state(InputForm.parking)
    await message.answer('Нужен ли паркинг?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.NEED_PARKING))


@router.callback_query(F.data.contains(f'{config.FEATURES.NEED_PARKING}:'), InputForm.parking)
async def step8(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    if choice == '1':
        await callback.message.edit_text('Паркинг: <i>Да</i>')
    elif choice == '0':
        await callback.message.edit_text('Паркинг: <i>Нет</i>')
    else:
        await callback.message.edit_text('Паркинг: <i>Не важно</i>')
    await state.update_data(parking=choice)
    await state.set_state(InputForm.num_balcony)
    await callback.message.answer('Сколько балконов в квартире?', reply_markup=kb.not_important_btn(config.FEATURES.NUM_BALCONY))


@router.callback_query(F.data.contains(f'{config.FEATURES.NUM_BALCONY}:'), InputForm.num_balcony)
async def step9(callback : CallbackQuery, state: FSMContext):
    await state.update_data(num_balcony='None')
    await callback.message.edit_text('Количество балконов: <i>Не важно</i>')
    await state.set_state(InputForm.num_cargo_elevators)
    await callback.message.answer('Сколько грузовых лифтов в доме?', reply_markup=kb.not_important_btn(config.FEATURES.NUM_CARGO_ELEVATORS))


@router.message(InputForm.num_balcony)
async def step9(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(num_balcony=message.text)
    await state.set_state(InputForm.num_cargo_elevators)
    await message.answer('Сколько грузовых лифтов в доме?',  reply_markup=kb.not_important_btn(config.FEATURES.NUM_CARGO_ELEVATORS))


@router.callback_query(F.data.contains(f'{config.FEATURES.NUM_CARGO_ELEVATORS}:'), InputForm.num_cargo_elevators)
async def step10(callback : CallbackQuery, state: FSMContext):
    await state.update_data(num_cargo_elevators='None')
    await callback.message.edit_text('Количество грузовых лифтов: <i>Не важно</i>')
    await state.set_state(InputForm.num_elevators)
    await callback.message.answer('Сколько пассажирских лифтов в доме?', reply_markup=kb.not_important_btn(config.FEATURES.NUM_ELEVATORS))


@router.message(InputForm.num_cargo_elevators)
async def step10(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(num_cargo_elevators=message.text)
    await state.set_state(InputForm.num_elevators)
    await message.answer('Сколько пассажирских лифтов в доме?', reply_markup=kb.not_important_btn(config.FEATURES.NUM_ELEVATORS))


@router.callback_query(F.data.contains(f'{config.FEATURES.NUM_ELEVATORS}:'), InputForm.num_elevators)
async def step11(callback : CallbackQuery, state: FSMContext):
    await state.update_data(num_elevators='None')
    await callback.message.edit_text('Количество пассажирских лифтов: <i>Не важно</i>')
    await state.set_state(InputForm.kitchen_area)
    await callback.message.answer('Какова площадь кухни?', reply_markup=kb.not_important_btn(config.FEATURES.KITCHEN_AREA))


@router.message(InputForm.num_elevators)
async def step11(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(num_elevators=message.text)
    await state.set_state(InputForm.kitchen_area)
    await message.answer('Какова площадь кухни?', reply_markup=kb.not_important_btn(config.FEATURES.KITCHEN_AREA))


@router.callback_query(F.data.contains(f'{config.FEATURES.KITCHEN_AREA}:'), InputForm.kitchen_area)
async def step12(callback : CallbackQuery, state: FSMContext):
    await state.update_data(kitchen_area='None')
    await callback.message.edit_text('Площадь кухни: <i>Не важно</i>')
    await state.set_state(InputForm.agent)
    await callback.message.answer('Продажа от агента?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.AGENT))


@router.message(InputForm.kitchen_area)
async def step12(message: Message, state: FSMContext):
    while not is_integer(message.text):
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
        return
    await state.update_data(kitchen_area=message.text)
    await state.set_state(InputForm.agent)
    await message.answer('Продажа от агента?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.AGENT))


@router.callback_query(F.data.contains(f'{config.FEATURES.AGENT}:'), InputForm.agent)
async def step13(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]

    if choice == '1':
        await callback.message.edit_text('Продажа от агента: <i>Да</i>')
    elif choice == '0':
        await callback.message.edit_text('Продажа от агента: <i>Нет</i>')
    else:
        await callback.message.edit_text('Продажа от агента: <i>Не важно</i>')
    await state.update_data(agent=choice)

    data = await state.get_data()
    for key, value in data.items():
        print(key, ' : ', value)
    await state.clear()


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
