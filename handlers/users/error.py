"""
Сообщение, которое будет вылазить при неизвестном боту сообщении
"""
from aiogram import types

from loader import dp
from keyboards.inline.help_buttons import help_keyboard, help_callback

game_guide = """
❓ КАК ИГРАТЬ ❓

Ваша основная задача - развивать свою ферму. Купите животных и собирайте с них ресурсы, которые в последствии можно будет продать.
Не забывайте про место в амбаре, которое уменьшается при каждом сборе ресурсов, а также восстанавливается после их продажи.
За каждые 100 очков опыта, вам будет даваться 1 уровень.
Успехов в игре!
"""

@dp.message_handler()
async def error(message: types.Message) -> None:
    await message.answer("😔 Прости, но ты по видимости ошибся в команде. Я не могу тебя понять. Вот, чем я могу тебе помочь 👇", reply_markup=help_keyboard)


@dp.callback_query_handler(help_callback.filter(btn="guide"))
async def user_guide(message: types.Message) -> None:
    await dp.bot.send_message(message.from_user.id, game_guide)


@dp.callback_query_handler(help_callback.filter(btn="commands"))
async def user_commands(message: types.Message) -> None:
    text = [
        '📝 Вот тебе список доступных команд: ',
        '/help - 📃 Список команд',
        '/profile - 👤 Перейти в профиль'
    ]
    await dp.bot.send_message(message.from_user.id, "\n".join(text))