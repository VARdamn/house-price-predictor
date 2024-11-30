from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
import os


class Settings(BaseSettings):

    ROOT: str = os.path.dirname(os.path.abspath(__file__))

    BOT_DIR: str = os.path.join(ROOT, 'bot')

    LOGS_DIR: str = os.path.join(ROOT, 'logs')

    DATA_DIR: str = os.path.join(ROOT, 'data')

    SRC_DIR: str = os.path.join(ROOT, 'src')

    ERROR_LOG_FILE: str = os.path.join(LOGS_DIR, 'error.log')

    CYAN_CSV_FILE: str = os.path.join(DATA_DIR, 'cyan_data.csv')

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=os.path.join(ROOT, ".env"))

    TELEGRAM_BOT_TOKEN: str

    CYAN_COOKIE: str


config = Settings()
