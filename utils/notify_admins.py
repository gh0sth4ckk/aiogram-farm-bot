import logging

from aiogram import Dispatcher

from config import admins

async def on_startup_notify(dp: Dispatcher) -> None:
    """Отправляет сообщения админам в чат, что бот успешно запущен"""
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "B0T УСПЕШНО ЗАПУЩЕН!")
        except Exception as err:
            logging.exception(err)