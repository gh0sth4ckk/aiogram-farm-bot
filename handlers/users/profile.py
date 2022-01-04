from aiogram import types
from aiogram.dispatcher.filters import Command

from aiogram.utils.markdown import hbold

from loader import dp
from models.get_user_info import get_resource

from level import update_level

from keyboards.inline.profile_buttons import profile_keyboard

@dp.message_handler(Command("profile"))
async def get_user_profile(message: types.Message) -> None:
    username = message.from_user.full_name
    userid = message.from_user.id

    update_level(userid) # обновляем уровень игрока

    level = get_resource(userid, "level")
    coins = get_resource(userid, "coins")
    wood = get_resource(userid, "wood")

    await message.answer("\n".join([
        f"Профиль игрока {hbold(username)}:",
        f"Уровень: {hbold(level)}",
        "\n",
        f"Монеты: {hbold(coins)}",
        f"Дерево: {hbold(wood)}",
    ]), reply_markup=profile_keyboard)