"""
Создание системных переменных.
"""

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from models.database import Database

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage() # OR RedisStorage2()
dp = Dispatcher(bot, storage=storage)
db = Database()