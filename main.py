import asyncio
import logging

from src.bot import main

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main.run())
