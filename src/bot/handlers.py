from aiogram import F
from aiogram import Router
from aiogram.filters import Command, CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import config
import src.bot.constants as C
import src.bot.keyboards as kb
from src.bot.states import InputForm

router = Router()


class IsInteger(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isdecimal()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(C.get_start_message(message.from_user.first_name), reply_markup=kb.basic)
    await state.clear()


@router.message(Command('info'))
async def cmd_info(message: Message, state: FSMContext):
    await message.answer(C.info_message)
    await state.clear()


@router.message(Command('help'))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer(C.get_help_message())
    await state.clear()


@router.message(Command('predict'))
async def cmd_predict(message: Message, state: FSMContext):
    await state.set_state(InputForm.district)
    await message.answer('Выберите административный округ:', reply_markup=kb.msk_districts)


@router.callback_query(F.data.startswith('district:'), InputForm.district)
async def ask_underground(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await callback.message.edit_text(f'Административный округ: <i>{choice}</i>')
    await state.update_data(district=choice)
    await state.set_state(InputForm.nearest_underground)
    await callback.message.answer('Сколько минут идти до метро?')


@router.message(InputForm.nearest_underground, IsInteger())
async def ask_rooms_count(message: Message, state: FSMContext):
    await state.update_data(nearest_underground=int(message.text))
    await state.set_state(InputForm.rooms_count)
    await message.answer('Сколько комнат в квартире?')


@router.message(InputForm.rooms_count, IsInteger())
async def ask_has_furniture(message: Message, state: FSMContext):
    await state.update_data(rooms_count=int(message.text))
    await state.set_state(InputForm.has_furniture)
    await message.answer('Есть ли мебель в квартире?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.HAS_FURNITURE))


@router.callback_query(F.data.contains(f'{config.FEATURES.HAS_FURNITURE}:'), InputForm.has_furniture)
async def ask_area(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await callback.message.edit_text(f'Есть ли мебель? <i>{C.boolean_map(choice)}</i>')
    await state.update_data(has_furniture=int(choice))
    await state.set_state(InputForm.area)
    await callback.message.answer('Какова площадь квартиры?')


@router.message(InputForm.area, IsInteger())
async def ask_living_area(message: Message, state: FSMContext):
    await state.update_data(area=int(message.text))
    await state.set_state(InputForm.living_area)
    await message.answer('Какова жилая площадь?')


@router.message(InputForm.living_area, IsInteger())
async def ask_kitchen_area(message: Message, state: FSMContext):
    await state.update_data(living_area=int(message.text))
    await state.set_state(InputForm.kitchen_area)
    await message.answer('Какова площадь кухни?')


@router.message(InputForm.kitchen_area, IsInteger())
async def ask_floors_count(message: Message, state: FSMContext):
    await state.update_data(kitchen_area=int(message.text))
    await state.set_state(InputForm.floors_count)
    await message.answer('Сколько этажей в доме?')


@router.message(InputForm.floors_count, IsInteger())
async def ask_floor(message: Message, state: FSMContext):
    await state.update_data(floors_count=int(message.text))
    await state.set_state(InputForm.floor)
    await message.answer('На каком этаже квартира?')


@router.message(InputForm.floor, IsInteger())
async def ask_parking_type(message: Message, state: FSMContext):
    floors_count = (await state.get_data()).get('floors_count', 0)
    while int(message.text) > floors_count:
        await message.answer(f'Этаж не может быть больше {floors_count}. Попробуйте снова.')
        return
    await state.update_data(floor=int(message.text))
    await state.set_state(InputForm.parking_type)
    await message.answer('Какой нужен паркинг?', reply_markup=kb.parking_type())


@router.callback_query(F.data.contains(config.FEATURES.PARKING_TYPE), InputForm.parking_type)
async def ask_has_balconies(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    _, choice, text = callback.data.split(':')
    await callback.message.edit_text(f'Паркинг: <i>{text}</i>')
    await state.update_data(parking_type=choice)
    await state.set_state(InputForm.has_balconies)
    await callback.message.answer('Нужен ли балкон в квартире?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.HAS_BALCONIES))


@router.callback_query(F.data.contains(config.FEATURES.HAS_BALCONIES), InputForm.has_balconies)
async def ask_lifts_count(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await state.update_data(has_balconies=int(choice))
    await callback.message.edit_text(f'Нужен балкон? <i>{C.boolean_map(choice)}</i>')
    await state.set_state(InputForm.lifts_count)
    await callback.message.answer('Сколько лифтов нужно?', reply_markup=kb.lifts_count())


@router.callback_query(F.data.contains(config.FEATURES.LIFTS_COUNT), InputForm.lifts_count)
async def ask_has_cargo_lifts(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await state.update_data(lifts_count=choice)
    await callback.message.edit_text(f'Количество лифтов: <i>{choice}</i>')
    await state.set_state(InputForm.has_cargo_lifts)
    await callback.message.answer('Нужен ли грузовой лифт?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.HAS_CARGO_LIFTS))


@router.callback_query(F.data.contains(config.FEATURES.HAS_CARGO_LIFTS), InputForm.has_cargo_lifts)
async def ask_is_seller_agent(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await state.update_data(has_cargo_lifts=int(choice))
    await callback.message.edit_text(f'Нужен ли грузовой лифт?: <i>{C.boolean_map(choice)}</i>')
    await state.set_state(InputForm.is_seller_agent)
    await callback.message.answer('Продажа от агента?', reply_markup=kb.boolean_keyboard(feature=config.FEATURES.IS_SELLER_AGENT))


@router.callback_query(F.data.contains(config.FEATURES.IS_SELLER_AGENT), InputForm.is_seller_agent)
async def calculate_predict(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choice = callback.data.split(':')[1]
    await callback.message.edit_text(f'Продажа от агента: <i>{C.boolean_map(choice)}</i>')
    await state.update_data(is_seller_agent=int(choice))

    data = await state.get_data()
    for key, value in data.items():
        print(key, ': ', value, type(value))
    await state.clear()


@router.callback_query()
async def callback_handler(callback: CallbackQuery):
    await callback.answer()

    if callback.data == 'help':
        await callback.message.answer(C.get_help_message())

    elif callback.data == 'info':
        await callback.message.answer(C.info_message)


@router.message(lambda message, state: True)
async def invalid_input(message: Message, state: FSMContext):

    form_integer_states = [
        InputForm.nearest_underground.state,
        InputForm.rooms_count.state,
        InputForm.area.state,
        InputForm.living_area.state,
        InputForm.kitchen_area.state,
        InputForm.floors_count.state,
        InputForm.floor.state,
    ]
    current_state = await state.get_state()

    if current_state in form_integer_states:
        await message.answer('<b>Пожалуйста, введите только целое число!</b>')
