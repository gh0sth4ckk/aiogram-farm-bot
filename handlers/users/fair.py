"""
Ярмарка для продажи ресурсов.
"""
from aiogram import types
from loader import dp, db

from keyboards.inline.profile_buttons import profile_callback
from keyboards.inline.fair_buttons import fair_callback, fair_keyboard

from models.get_user_info import get_item, get_resource

from level import give_points

# стоимость ресурсов в монетах
one_wool_cost = 2
one_egg_cost = 4
one_milk_cost = 7

@dp.callback_query_handler(profile_callback.filter(btn="fair"))
async def fair(message: types.Message) -> None:
    """Главная функция ярмарки."""
    global wool_for_sale
    global eggs_for_sale
    global milk_for_sale

    userid = message.from_user.id
    user_wool = get_item(userid, "wool")
    user_eggs = get_item(userid, "egg")
    user_milk = get_item(userid, "milk")

    # Количество монет которое можно получить при продаже
    # кол-во ресурса у игрока * стоимость одного ресурса
    wool_for_sale = user_wool * one_wool_cost
    eggs_for_sale = user_eggs * one_egg_cost
    milk_for_sale = user_milk * one_milk_cost

    msg = f"""
Добро пожаловать на ярмарку! Здесь, ты можешь продать свои ресурсы и получить за это деньги.
1 шерсть - {one_wool_cost} монеты
1 яйцо - {one_egg_cost} монеты
1 молоко - {one_milk_cost} монет

Вы можете продать...
Шерсть за {wool_for_sale} монет 
Яйца за {eggs_for_sale} монет
Молоко за {milk_for_sale} монет
"""

    await dp.bot.send_message(message.from_user.id, msg, reply_markup=fair_keyboard)


# ПРОДАТЬ ШЕРСТЬ
@dp.callback_query_handler(fair_callback.filter(product="wool"))
async def wool_sale(call: types.CallbackQuery) -> None:
    wool = get_item(call.from_user.id, "wool")
    db.execute(f"UPDATE user_items SET wool = 0 WHERE user_id=?", params=(call.from_user.id, ), commit=True) # Убираем всю шерсть
    db.execute(f"UPDATE users SET coins = coins + {wool_for_sale} WHERE id=?", params=(call.from_user.id, ), commit=True) # Добавляем деньги
    db.execute(f"UPDATE users SET barn_accumulation =  barn_accumulation + {wool} WHERE id=?", params=(call.from_user.id, ), commit=True) # Добавляем место в амбар
    give_points(call.from_user.id, 15)
    await call.answer("Шерсть успешно продана! Вы получили 15 очков опыта")


# ПРОДАТЬ ЯЙЦА
@dp.callback_query_handler(fair_callback.filter(product="eggs"))
async def wool_sale(call: types.CallbackQuery) -> None:
    eggs = get_item(call.from_user.id, "egg")
    db.execute(f"UPDATE user_items SET egg = 0 WHERE user_id=?", params=(call.from_user.id, ), commit=True) # Убираем все яйца
    db.execute(f"UPDATE users SET coins = coins + {eggs_for_sale} WHERE id=?", params=(call.from_user.id, ), commit=True) # Добавляем деньги
    db.execute(f"UPDATE users SET barn_accumulation =  barn_accumulation + {eggs} WHERE id=?", params=(call.from_user.id, ), commit=True) # Добавляем место в амбар
    give_points(call.from_user.id, 30)
    await call.answer("Яйца успешно проданы! Вы получили 30 очков опыта")


# ПРОДАТЬ МОЛОКО
@dp.callback_query_handler(fair_callback.filter(product="milk"))
async def wool_sale(call: types.CallbackQuery) -> None:
    milk = get_item(call.from_user.id, "milk")
    db.execute(f"UPDATE user_items SET milk = 0 WHERE user_id=?", params=(call.from_user.id, ), commit=True) # Убираем всё молоко
    db.execute(f"UPDATE users SET coins = coins + {milk_for_sale} WHERE id=?", params=(call.from_user.id, ), commit=True) # Добавляем деньги
    db.execute(f"UPDATE users SET barn_accumulation =  barn_accumulation + {milk} WHERE id=?", params=(call.from_user.id, ), commit=True) # Добавляем место в амбар
    give_points(call.from_user.id, 50)
    await call.answer("Молоко успешно продано! Вы получили 50 очков опыта")