import os
from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class FeaturesModel(BaseModel):

    HAS_FURNITURE: str = 'has_furniture'

    PARKING_TYPE: str = 'parking_type'

    IS_SELLER_AGENT: str = 'is_seller_agent'

    FLOOR: str = 'floor'

    FLOORS_COUNT: str = 'floors_count'

    HAS_BALCONIES: str = 'has_balconies'

    LIFTS_COUNT: str = 'lifts_count'

    HAS_CARGO_LIFTS: str = 'has_cargo_lifts'

    KITCHEN_AREA: str = 'kitchen_area'


class Settings(BaseSettings):

    ROOT: str = os.path.dirname(os.path.abspath(__file__))

    BOT_DIR: str = os.path.join(ROOT, 'bot')

    LOGS_DIR: str = os.path.join(ROOT, 'logs')

    DATA_DIR: str = os.path.join(ROOT, 'data')

    SRC_DIR: str = os.path.join(ROOT, 'src')

    ERROR_LOG_FILE: str = os.path.join(LOGS_DIR, 'error.log')

    CYAN_CSV_FILE: str = os.path.join(DATA_DIR, 'cyan_data.csv')

    FEATURES: FeaturesModel = FeaturesModel()

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=os.path.join(ROOT, '.env'))

    TELEGRAM_BOT_TOKEN: str

    CYAN_COOKIE: str


config = Settings()
