"""
Стартовый файл запуска B0T'a
"""
from loader import dp

async def on_startup(dp) -> None:
    """Функция сработает при включении бота."""
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    

    from utils.notify_admins import on_startup_notify
    from utils.set_bot_commands import set_default_commands
    await on_startup_notify(dp)     # Установка админского оповещения при включении бота
    await set_default_commands(dp)  # Установка команд которые будут видны при нажатии "/"


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
