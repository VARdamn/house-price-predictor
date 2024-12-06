from aiogram import Bot
from aiogram import Dispatcher

from config import config
from src.bot.handlers import router

dp = Dispatcher()
bot = Bot(token=config.TELEGRAM_BOT_TOKEN)


async def run():
    dp.include_router(router)
    await dp.start_polling(bot)
