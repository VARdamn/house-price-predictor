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

    SRC_DIR: str = os.path.join(ROOT, 'src')

    MODELING_DIR: str = os.path.join(SRC_DIR, 'modeling')

    LOGS_DIR: str = os.path.join(ROOT, 'logs')

    DATA_DIR: str = os.path.join(ROOT, 'data')

    ERROR_LOG_FILE: str = os.path.join(LOGS_DIR, 'error.log')

    CYAN_CSV_FILE: str = os.path.join(DATA_DIR, 'cyan_data.csv')

    PIPELINE_FILE: str = os.path.join(MODELING_DIR, 'pipeline.joblib')

    FEATURES: FeaturesModel = FeaturesModel()

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=os.path.join(ROOT, '.env'))

    TELEGRAM_BOT_TOKEN: str

    CYAN_COOKIE: str


config = Settings()
