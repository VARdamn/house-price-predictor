from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class InputForm(StatesGroup):
    floor = State()
    num_floors = State()
    area = State()
    living_area = State()  # ?
    kitchen_area = State()
    num_rooms = State()
    with_furniture = State()
    address = State()  # ?
    ao = State()
    metro = State()
    price_per_month = State()  # ?
    num_balcony = State()
    agent = State()
    num_cargo_elevators = State()
    num_elevators = State()
    parking = State()
