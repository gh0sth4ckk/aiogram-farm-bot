from aiogram import types

from loader import dp
from keyboards.inline.profile_buttons import profile_callback

@dp.callback_query_handler(profile_callback.filter(btn="donate"))
async def user_donate(message: types.Message) -> None:
    await message.answer("donate...")