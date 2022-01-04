from aiogram import types

from loader import dp, db

from keyboards.inline.profile_buttons import profile_callback

from keyboards.inline.shop_buttons import shop_callback, shop_keyboard
from keyboards.inline.shop_buttons import wood_callback, wood_shop_keyboard
from keyboards.inline.shop_buttons import barn_callback, barn_shop_keyboard
from keyboards.inline.shop_buttons import houses_callback, house_shop_keyboard
from keyboards.inline.shop_buttons import animals_callback, animals_shop_keyboard

from models.get_user_info import get_resource

from aiogram.utils.markdown import hbold


@dp.callback_query_handler(profile_callback.filter(btn="shop"))
async def user_shop(call: types.CallbackQuery) -> None:
    await dp.bot.send_message(call.from_user.id, "В магазине, ты можешь купить животных и дома. А также, дополнительное место в амбаре и доски.", reply_markup=shop_keyboard)


# ПОКУПКА БРЕВЕН
wood_cost = 20
@dp.callback_query_handler(shop_callback.filter(shop_type="wood"))
async def shop_wood(call: types.CallbackQuery) -> None:
    await call.message.answer(f"5 досок стоят <b>{wood_cost}</b> монет 🪙", reply_markup=wood_shop_keyboard)

@dp.callback_query_handler(wood_callback.filter(wood="wood"))
async def wood_buying(call: types.CallbackQuery) -> None:
    user_coins = get_resource(call.from_user.id, "coins")
    if not user_coins < wood_cost:
        db.execute(f"UPDATE users SET coins = coins - {wood_cost} WHERE id=?", params=(call.from_user.id, ), commit=True) # Забираем монеты у пользователя
        db.execute(f"UPDATE users SET wood = wood + 5 WHERE id=?", params=(call.from_user.id, ), commit=True) # Даем пользователю доски
        await call.answer("✅ Вы купили 5 досок")
        await call.answer()
    else:
        await call.answer("❌ У вас недостаточно денег для покупки досок")
        await call.answer()

# ПОКУПКА МЕСТА В АМБАРЕ
barn_place_cost = 40
@dp.callback_query_handler(shop_callback.filter(shop_type="barn"))
async def shop_barn(call: types.CallbackQuery) -> None:
    await call.message.answer(f"Дополнительные 10 мест в амбаре стоят <b>{barn_place_cost}</b> монет 🪙", reply_markup=barn_shop_keyboard)

@dp.callback_query_handler(barn_callback.filter(barn="barn"))
async def barn_buying(call: types.CallbackQuery) -> None:
    user_coins = get_resource(call.from_user.id, "coins")
    if not user_coins < barn_place_cost:
        db.execute(f"UPDATE users SET coins = coins - {barn_place_cost} WHERE id=?", params=(call.from_user.id, ), commit=True) # Забираем монеты у пользователя
        db.execute(f"UPDATE users SET barn_accumulation = barn_accumulation + 10 WHERE id=?", params=(call.from_user.id, ), commit=True) # Даем пользователю доп. место
        await call.answer("✅ Вы купили 10 дополнительных мест в амбаре")
        await call.answer()
    else:
        await call.answer("❌ У вас недостаточно денег для покупки дополнительного места в амбаре")
        await call.answer()


# МАГАЗИН ДОМОВ
chicken_coop_coins_cost = 30 # Стоимость курятника в монетах
chicken_coop_wood_cost = 20 # Стоимость курятника в досках

cowshed_coins_cost = 60 # Стоимость коровника в монетах
cowshed_wood_cost = 45 # Стоимость коровника в досках

@dp.callback_query_handler(shop_callback.filter(shop_type="houses"))
async def shop_houses(call: types.CallbackQuery) -> None:
    building_list = f"""
Вот, что мы можем вам предложить:

1. Курятник - {hbold(chicken_coop_coins_cost)} монет 🪙, {hbold(chicken_coop_wood_cost)} дерева 🪵
2. Коровник - {hbold(cowshed_coins_cost)} монет 🪙, {hbold(cowshed_wood_cost)} дерева 🪵
    """
    await call.message.answer(building_list, reply_markup=house_shop_keyboard)


@dp.callback_query_handler(houses_callback.filter(house_type="chicken_coop"))
async def chicken_coop_buy(call: types.CallbackQuery) -> None:
    """Покупка курятника"""
    user_coins = get_resource(call.from_user.id, "coins")
    user_wood = get_resource(call.from_user.id, "wood")

    user_chicken_coop = db.execute("SELECT chicken_coop FROM buildings WHERE user_id=?", params=(call.from_user.id, ), fethcone=True)[0]

    if not user_coins < chicken_coop_coins_cost and not user_wood < chicken_coop_wood_cost: # Проверка на деньги и доски
        if user_chicken_coop == 0: # Проверка на отстутствие курятника
            db.execute(f"UPDATE users SET coins = coins - {chicken_coop_coins_cost} WHERE id=?", params=(call.from_user.id, ), commit=True) # Забираем деньги
            db.execute(f"UPDATE users SET wood = wood - {chicken_coop_wood_cost} WHERE id=?", params=(call.from_user.id, ), commit=True)
            db.execute("UPDATE buildings SET chicken_coop = 1 WHERE user_id=?", params=(call.from_user.id, ), commit=True) # Устанавливаем курятник
            await call.message.answer("✅ Вы купили курятник!")
            await call.message.delete_reply_markup()
        else:
            await call.answer("❌ У вас уже есть курятник")
    else:
        await call.answer("❌ У вас недостаточно денег или дерева, чтобы купить курятник")


@dp.callback_query_handler(houses_callback.filter(house_type="cowshed"))
async def cowshed_buy(call: types.callback_query) -> None:
    """Покупка коровника"""
    user_coins = get_resource(call.from_user.id, "coins")
    user_wood = get_resource(call.from_user.id, "wood")

    user_cowshed = db.execute("SELECT cowshed FROM buildings WHERE user_id=?", params=(call.from_user.id, ), fethcone=True)[0]

    if not user_coins < cowshed_coins_cost and not user_wood < cowshed_wood_cost: # Проверка на деньги и доски
        if user_cowshed == 0: # Проверка на отстутствие коровника
            db.execute(f"UPDATE users SET coins = coins - {cowshed_coins_cost} WHERE id=?", params=(call.from_user.id, ), commit=True) # Забираем деньги
            db.execute(f"UPDATE users SET wood = wood - {cowshed_wood_cost} WHERE id=?", params=(call.from_user.id, ), commit=True)
            db.execute("UPDATE buildings SET cowshed = 1 WHERE user_id=?", params=(call.from_user.id, ), commit=True) # Устанавливаем коровник
            await call.message.answer("✅ Вы купили коровник!")
            await call.message.delete_reply_markup()
        else:
            await call.answer("❌ У вас уже есть коровник")
    else:
        await call.answer("❌ У вас недостаточно денег или дерева, чтобы купить коровник")



# МАГАЗИН ЖИВОТНЫХ
sheep_cost = 10 # Стоимость овцы
chicken_cost = 16 # Стоимость курицы
cow_cost = 27 # Стоимость коровы

@dp.callback_query_handler(shop_callback.filter(shop_type="animals"))
async def shop_animals(call: types.Message) -> None:
    animals_list = f"""
Вот, что мы можем вам предложеть:

1. 🐑 Овца {hbold(sheep_cost)} монет/шт
2. 🐔 Курица {hbold(chicken_cost)} монет/шт
3. 🐮 Корова {hbold(cow_cost)} монет/шт
    """
    await dp.bot.send_message(call.from_user.id, animals_list, reply_markup=animals_shop_keyboard)



@dp.callback_query_handler(animals_callback.filter(animal="sheep"))
async def sheep_buying(call: types.CallbackQuery) -> None:
    """Покупка овцы"""
    user_coins = get_resource(call.from_user.id, "coins")

    if not user_coins < sheep_cost:
        db.execute(f"UPDATE users SET coins = coins - {sheep_cost} WHERE id=?", params=(call.from_user.id, ), commit=True) # Забираем деньги у пользователя
        db.execute(f"UPDATE animals SET sheep = sheep + 1 WHERE user_id=?", params=(call.from_user.id, ), commit=True)
        await call.answer("✅ Вы купили одну овцу")
        await call.answer()
    else:
        await call.answer("❌ Вам не хватает денег")


@dp.callback_query_handler(animals_callback.filter(animal="chicken"))
async def chicken_buying(call: types.CallbackQuery) -> None:
    """Покупка курицы"""
    user_coins = get_resource(call.from_user.id, "coins")

    if not user_coins < chicken_cost:
        db.execute(f"UPDATE users SET coins = coins - {chicken_cost} WHERE id=?", params=(call.from_user.id, ), commit=True) # Забираем деньги у пользователя
        db.execute(f"UPDATE animals SET chicken = chicken + 1 WHERE user_id=?", params=(call.from_user.id, ), commit=True)
        await call.answer("✅ Вы купили одну курицу")
        await call.answer()
    else:
        await call.answer("❌ Вам не хватает денег")


@dp.callback_query_handler(animals_callback.filter(animal="cow"))
async def cow_buying(call: types.CallbackQuery) -> None:
    """Покупка коровы"""
    user_coins = get_resource(call.from_user.id, "coins")

    if not user_coins < cow_cost:
        db.execute(f"UPDATE users SET coins = coins - {cow_cost} WHERE id=?", params=(call.from_user.id, ), commit=True) # Забираем деньги у пользователя
        db.execute(f"UPDATE animals SET cow = cow + 1 WHERE user_id=?", params=(call.from_user.id, ), commit=True)
        await call.answer("✅ Вы купили одну корову")
        await call.answer()
    else:
        await call.answer("❌ Вам не хватает денег")
