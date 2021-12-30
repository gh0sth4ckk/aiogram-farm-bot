from aiogram import types
from aiogram.dispatcher.filters import Command

from aiogram.utils.markdown import hbold

from loader import dp
from models.get_user_info import get_resource

from keyboards.inline.profile_keyboard import profile_keyboard

@dp.message_handler(Command("profile"))
async def get_user_profile(message: types.Message) -> None:
    username = message.from_user.full_name
    userid = message.from_user.id

    level = get_resource(userid, "level")
    coins = get_resource(userid, "coins")
    wood = get_resource(userid, "wood")
    food = get_resource(userid, "food")

    await message.answer("\n".join([
        f"Профиль игрока {hbold(username)}:",
        f"Уровень: {hbold(level)}",
        "\n",
        f"Монеты: {hbold(coins)}",
        f"Дерево: {hbold(wood)}",
        f"Еда: {hbold(food)}",
    ]), reply_markup=profile_keyboard)