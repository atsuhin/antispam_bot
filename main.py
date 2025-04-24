import logging
from aiogram import Dispatcher, types, Bot, executor
import config as conf

logging.basicConfig(level = logging.INFO)

bot = Bot(token = conf.TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)