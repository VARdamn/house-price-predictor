from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class InputForm(StatesGroup):
    district = State()
    nearest_underground = State()
    rooms_count = State()
    has_furniture = State()
    area = State()
    floors_count = State()
    floor = State()
    living_area = State()
    kitchen_area = State()
    has_balconies = State()
    is_seller_agent = State()
    lifts_count = State()
    has_cargo_lifts = State()
    parking_type = State()
