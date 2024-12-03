from aiogram import Bot, Dispatcher
from config import config
from src.bot.handlers import router

dp = Dispatcher()

async def run():
    dp.include_router(router)
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    await dp.start_polling(bot)

