from aiogram import types

from loader import dp
from keyboards.inline.profile_keyboard import profile_callback

@dp.callback_query_handler(profile_callback.filter(btn="shop"))
async def user_shop(message: types.Message) -> None:
    await message.answer("shop...")