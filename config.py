from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar
import os


class Settings(BaseSettings):

    ROOT: str = os.path.dirname(os.path.abspath(__file__))

    BOT_ROOT: str = os.path.join(ROOT, 'bot')

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=os.path.join(ROOT, ".env"))

    TELEGRAM_BOT_TOKEN: str

    CYAN_API_KEY: str


config = Settings()
