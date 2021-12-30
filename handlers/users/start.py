from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from aiogram.utils.markdown import hbold

from loader import dp, db


@dp.message_handler(CommandStart(deep_link="refer-link"))
async def bot_start_bonus(message: types.Message) -> None:
    user_id = message.from_user.id
    user_fullname = message.from_user.full_name

    # дополнительные ресурсы
    coins_vip = 150
    wood_vip = 150
    barn_accamulation_vip = 50

    level = 0
    coins = 200
    wood = 100
    barn_accamulation = 150

    greeting_text = f"""
Ого, {hbold(user_fullname)}, вот это да! Ты перешел по специальной ссылке и теперь, можешь забрать свои долгожданные бонусы! Добро пожаловать!

Здесь ты сможешь развивать свою ферму, следить за животными и получать за это прибыль. Приятного время препровождения, {user_fullname}!

Вот тебе ресуры для начала:
Монеты: {hbold(coins)} + {hbold(coins_vip)} дополнительных монет
Дерево: {hbold(wood)} + {hbold(wood_vip)} дополнительного дерева
Вместиость амбара: {hbold(barn_accamulation)} + {hbold(barn_accamulation_vip)} дополнительного места

Пиши /profile, чтобы перейти в профиль. Встретимся там!
    """
    if db.execute("SELECT id FROM users WHERE id=?", params=(user_id, ), fethcone=True):
        await message.answer("Сэр, но вы не можете начать все сначала!")
    else:
        db.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, )", params=(user_id, user_fullname, level, coins+coins_vip, wood+wood_vip, barn_accamulation+barn_accamulation_vip), commit=True)
        db.execute("INSERT INTO buildings VALUES(?, ?, ?, ?, ?)", params=(user_id, 1, 1, 0, 0), commit=True)
        db.execute("INSERT INTO animals VALUES(?, ?, ?, ?)", params=(user_id, 0, 0, 0), commit=True)
        db.execute("INSERT INTO user_items VALUES(?, ?, ?, ?)", params=(user_id, 0, 0, 0), commit=True)
        db.execute("INSERT INTO temp_items VALUES(?, ?, ?, ?)", params=(user_id, 0, 0, 0), commit=True)
        await message.answer(greeting_text)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message) -> None:
    user_id = message.from_user.id
    user_fullname = message.from_user.full_name
    level = 0
    coins = 200
    wood = 100
    barn_accamulation = 150

    greeting_text = f"""
Дорогой, {hbold(user_fullname)}! Рад приветствовать тебя здесь, в этом чудесном месте!

Здесь ты сможешь развивать свою ферму, следить за животными и получать за это прибыль. Приятного время препровождения, {user_fullname}, ещё свидимся!

Вот тебе ресуры для начала:
Монеты: {hbold(coins)}
Дерево: {hbold(wood)}
Вместиость амбара: {hbold(barn_accamulation)}

Пиши /profile, чтобы перейти в профиль. Встретимся там!
    """

    if db.execute("SELECT id FROM users WHERE id=?", params=(user_id, ), fethcone=True):
        await message.answer("Сэр, вы не можете начать все сначала!")
    else:
        db.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", params=(user_id, user_fullname, level, coins, wood, barn_accamulation), commit=True)
        db.execute("INSERT INTO buildings VALUES(?, ?, ?, ?, ?)", params=(user_id, 1, 1, 0, 0), commit=True)
        db.execute("INSERT INTO animals VALUES(?, ?, ?, ?)", params=(user_id, 0, 0, 0), commit=True)
        db.execute("INSERT INTO user_items VALUES(?, ?, ?, ?)", params=(user_id, 0, 0, 0), commit=True)
        db.execute("INSERT INTO temp_items VALUES(?, ?, ?, ?)", params=(user_id, 0, 0, 0), commit=True)
        await message.answer(greeting_text)