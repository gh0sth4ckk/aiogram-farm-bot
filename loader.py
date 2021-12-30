"""
Создание системных переменных.
"""
import time

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from models.database import Database

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage() # OR RedisStorage2()
dp = Dispatcher(bot, storage=storage)
db = Database()


def farm(dp, var) -> None:
    while var:
        time.sleep(4)
        message = types.Message
        print("start")
        #wool_for_catch = db.execute("SELECT wool FROM temp_items WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0]
        #db.execute(f"UPDATE temp_items SET wool = {wool_for_catch + 10} WHERE user_id=?", params=(message.from_user.id, ), commit=True)