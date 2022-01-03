from aiogram import types
from aiogram.types import message
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hbold

from loader import dp, db

from keyboards.inline.profile_buttons import profile_callback
from keyboards.default.farm_keyboard import farm_keyboard

from models.get_user_info import get_resource, get_animals


@dp.callback_query_handler(profile_callback.filter(btn="farm"))
async def user_farm(message: types.Message) -> None:
    """Главное меню фермы."""
    username = message.from_user.full_name
    userid = message.from_user.id

    barn_accumulation = get_resource(userid, "barn_accumulation")

    builds = db.execute(sql="SELECT house, barn, chicken_coop, cowshed FROM buildings WHERE user_id=?", params=(userid, ), fetchall=True)
    animals = db.execute(sql="SELECT sheep, chicken, cow FROM animals WHERE user_id=?", params=(userid, ), fetchall=True)

    builds_count = sum(builds[0])
    animals_count = sum(animals[0])

    farm = f"""
Ферма игрока {hbold(username)}:

Свободного места в амбаре: {hbold(barn_accumulation)}

Общее кол-во построек:  {hbold(builds_count)}
Общее кол-во животных:  {hbold(animals_count)}
    """

    await dp.bot.send_message(message.from_user.id, farm, reply_markup=farm_keyboard)


# ================ САД ================
sheep_callback = CallbackData("sheep", "get_wool") # Коллбэк для кнопки сбора и добычи шерсти

@dp.message_handler(text="Сад")
async def garden(message: types.Message) -> None:
    """Это основная функция сада. Здесь можно посмотреть количество ваших овец, а также вы можете собрать всю накопившуюся шерсть."""
    global wool_count, wool_for_catch # Глобально объявляем количетсво нашей шерсти и шерсти, которую можно собрать

    sheep_count = get_animals(message.from_user.id, "sheep") # Получаем количество наших овец
    
    # Наша шерсть, которая занимает место в амбаре и которую в дальнейшем можно продать
    wool_count = db.execute("SELECT wool FROM user_items WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0]
    # Шерсть которую можно собрать, она не занимает в амбаре место и её нельзя продать
    wool_for_catch = db.execute("SELECT wool FROM temp_items WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0]
    await message.answer("\n".join([
        f"{hbold('Задний двор:')}",
        f"Количетсво овец: {hbold(sheep_count)}",
        "\n",
        f"Количество вашей шерсти: {hbold(wool_count)}",
        f"Доступно шерсти для сбора: {hbold(wool_for_catch)}"
    ]), reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[ # Создаем клавиатуру для функции сбора шерсти
        [InlineKeyboardButton(text="Добыть шерсть", callback_data=sheep_callback.new("get")), InlineKeyboardButton(text="Собрать шерсть", callback_data=sheep_callback.new("cath"))]
    ]))
    await message.delete()

@dp.callback_query_handler(sheep_callback.filter(get_wool="get"))
async def get_wool(call: types.CallbackQuery) -> None:
    """Функция получения шерсти."""
    sheep_give = get_animals(call.from_user.id, "sheep") # Сколько дает овца за один сбор
    if db.execute("SELECT sheep FROM animals WHERE user_id=?", params=(call.from_user.id, ), fethcone=True)[0] >= 1: # проверяем количество овец
        wool_for_catch = db.execute("SELECT wool FROM temp_items WHERE user_id=?", params=(call.from_user.id, ), fethcone=True)[0] # шерсть для сбора
        db.execute(f"UPDATE temp_items SET wool = {wool_for_catch + sheep_give} WHERE user_id=?", params=(call.from_user.id, ), commit=True) # добавляем добытую шерсть
        await call.answer(f"Вы добыли {sheep_give} шерсть(-и)")
        await call.answer()
    else:
        await call.answer("У вас нет овец, чтобы добывать шерсть")
        await call.answer()

@dp.callback_query_handler(sheep_callback.filter(get_wool="cath"))
async def catch_wool(call: types.CallbackQuery) -> None:
    """Функция сбора шерсти."""
    sheep_give = get_animals(call.from_user.id, "sheep")
    barn_accumulation = get_resource(call.from_user.id, "barn_accumulation") # 150
    if db.execute("SELECT barn_accumulation FROM users WHERE id=?", params=(call.from_user.id, ), fethcone=True)[0] > sheep_give: # Проверяем место в амбаре
        if wool_for_catch >= 1: # Проверяем количество шерсти. Должна быть хотя-бы одна штука
            db.execute(f"UPDATE user_items SET wool = {wool_count + wool_for_catch} WHERE user_id=?", params=(call.from_user.id, ), commit=True) # Добавляем шерсть игроку в амбар
            db.execute(f"UPDATE users SET barn_accumulation = barn_accumulation - {wool_for_catch}", commit=True) # Убираем место из амбара
            db.execute(f"UPDATE temp_items SET wool = 0 WHERE user_id=?", params=(call.from_user.id, ), commit=True) # Обнуляем временную шерсть
            await call.answer("Вы успешно собрали всю шерсть!")
            await call.answer()
        else:
            await call.answer("Нечего собирать")
            await call.answer()
    else:
        await call.answer("Вам не хватает места в амбаре")
        await call.answer()
# ================================================


# ================ КУРЯТНИК ================
chicken_callback = CallbackData("chicken", "get_eggs") # Коллбэк для кнопки сбора и добычи яиц

@dp.message_handler(text="Курятник")
async def chicken_coop(message: types.Message) -> None:
    """Основная функция курятника."""
    if db.execute("SELECT chicken_coop FROM buildings WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0] == 1:
        global eggs_count, eggs_for_catch
        chicken_count = get_animals(message.from_user.id, "chicken") # Получаем количество наших куриц

        # Наша шерсть, которая занимает место в амбаре и которую в дальнейшем можно продать
        eggs_count = db.execute("SELECT egg FROM user_items WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0]
        # Шерсть которую можно собрать, она не занимает в амбаре место и её нельзя продать
        eggs_for_catch = db.execute("SELECT egg FROM temp_items WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0]

        await message.answer("\n".join([
        f"{hbold('Курятник:')}",
        f"Количетсво куриц: {hbold(chicken_count)}",
        "\n",
        f"Количество ваших яиц: {hbold(eggs_count)}",
        f"Доступно яиц для сбора: {hbold(eggs_for_catch)}"
    ]), reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[ # Создаем клавиатуру для функции сбора шерсти
        [InlineKeyboardButton(text="Добыть яйца", callback_data=chicken_callback.new("get")), InlineKeyboardButton(text="Собрать яйца", callback_data=chicken_callback.new("cath"))]
    ]))
        await message.delete()
    else:
        await message.answer("Вы не преобрели ни одного курятника")
        await message.delete()

@dp.callback_query_handler(chicken_callback.filter(get_eggs="get"))
async def get_eggs(call: types.CallbackQuery) -> None:
    """Функция получения яиц."""
    chicken_give = get_animals(call.from_user.id, "chicken")
    if db.execute("SELECT chicken FROM animals WHERE user_id=?", params=(call.from_user.id, ), fethcone=True)[0] >= 1: # Проверяем количество куриц
        eggs_for_catch = db.execute("SELECT egg FROM temp_items WHERE user_id=?", params=(call.from_user.id, ), fethcone=True)[0]
        db.execute(f"UPDATE temp_items SET egg = {eggs_for_catch + chicken_give} WHERE user_id=?", params=(call.from_user.id, ), commit=True) # Добываем яйца
        await call.answer(f"Вы добыли {chicken_give} яиц")
        await message.answer()
    else:
        await call.answer("У вас нет куриц, чтобы добывать яйца")
        await message.answer()

@dp.callback_query_handler(chicken_callback.filter(get_eggs="cath"))
async def catch_eggs(message: types.Message) -> None:
    """Функция сбора яиц."""
    chicken_give = get_animals(message.from_user.id, "chicken")
    barn_accumulation = get_resource(message.from_user.id, "barn_accumulation") # 150
    if db.execute("SELECT barn_accumulation FROM users WHERE id=?", params=(message.from_user.id, ), fethcone=True)[0] > chicken_give: # Проверяем место в амбаре
        if eggs_for_catch >= 1: # Проверяем количество яиц. Должна быть хотя-бы одна штука
            db.execute(f"UPDATE user_items SET milk = {eggs_count + eggs_for_catch} WHERE user_id=?", params=(message.from_user.id, ), commit=True) # добавляем яйца игроку
            db.execute(f"UPDATE users SET barn_accumulation = {barn_accumulation - eggs_for_catch}", commit=True) # Убираем место из амбара
            db.execute(f"UPDATE temp_items SET milk = 0 WHERE user_id=?", params=(message.from_user.id, ), commit=True) # обнуляем временные яйца
            await message.answer("Вы успешно собрали все яйца!")
            await message.answer()
        else:
            await message.answer("Нечего собирать")
            await message.answer()
    else:
        await message.answer("Вам не хватает места в амбаре")
        await message.answer()
# =====================================================================


# ================ КОРОВНИК ================
cow_callback = CallbackData("cow", "get_milk") # Коллбэк для кнопки сбора и добычи молоко

@dp.message_handler(text="Коровник")
async def cowshed(message: types.Message) -> None:
    """Основная функция коровника"""
    if db.execute("SELECT cowshed FROM buildings WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0] == 1:
        global milk_count, milk_for_catch
        cows_count = get_animals(message.from_user.id, "cow") # Получаем количество наших коров

        # Наша шерсть, которая занимает место в амбаре и которую в дальнейшем можно продать
        milk_count = db.execute("SELECT milk FROM user_items WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0]
        # Шерсть которую можно собрать, она не занимает в амбаре место и её нельзя продать
        milk_for_catch = db.execute("SELECT milk FROM temp_items WHERE user_id=?", params=(message.from_user.id, ), fethcone=True)[0]

        await message.answer("\n".join([
        f"{hbold('Коровник:')}",
        f"Количетсво коров: {hbold(cows_count)}",
        "\n",
        f"Количество вашего молока: {hbold(milk_count)}мл",
        f"Доступно молока для сбора: {hbold(milk_for_catch)}мл"
    ]), reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[ # Создаем клавиатуру для функции сбора шерсти
        [InlineKeyboardButton(text="Добыть молоко", callback_data=cow_callback.new("get")), InlineKeyboardButton(text="Собрать молко", callback_data=cow_callback.new("cath"))]
    ]))
        await message.delete()
    else:
        await message.answer("Вы не преобрели ни одного коровника")
        await message.delete()

@dp.callback_query_handler(cow_callback.filter(get_milk="get"))
async def get_milk(call: types.CallbackQuery) -> None:
    """Функция получения молока."""
    cow_give = get_animals(call.from_user.id, "cow")
    if db.execute("SELECT cow FROM animals WHERE user_id=?", params=(call.from_user.id, ), fethcone=True)[0] >= 1: # проверяем количество коров
        milk_for_catch = db.execute("SELECT milk FROM temp_items WHERE user_id=?", params=(call.from_user.id, ), fethcone=True)[0]
        db.execute(f"UPDATE temp_items SET milk = {milk_for_catch + cow_give} WHERE user_id=?", params=(call.from_user.id, ), commit=True)
        await call.answer(f"Вы добыли {cow_give}мл молока")
        await message.answer()
    else:
        await call.answer("У вас нет коров, чтобы добывать молоко")
        await message.answer()

@dp.callback_query_handler(cow_callback.filter(get_milk="cath"))
async def catch_milk(message: types.Message) -> None:
    """Функция сбора молока."""
    cow_give = get_animals(message.from_user.id, "cow")
    barn_accumulation = get_resource(message.from_user.id, "barn_accumulation") # 150
    if db.execute("SELECT barn_accumulation FROM users WHERE id=?", params=(message.from_user.id, ), fethcone=True)[0] > cow_give: # Проверяем место в амбаре
        if milk_for_catch >= 1: # Проверяем количество молока. Должна быть хотя-бы одна штука
            db.execute(f"UPDATE user_items SET milk = {milk_count + milk_for_catch} WHERE user_id=?", params=(message.from_user.id, ), commit=True)
            db.execute(f"UPDATE users SET barn_accumulation = {barn_accumulation - milk_for_catch}", commit=True) # Убираем место из амбара
            db.execute(f"UPDATE temp_items SET milk = 0 WHERE user_id=?", params=(message.from_user.id, ), commit=True)
            await message.answer("Вы успешно собрали все молоко!")
            await message.answer()
        else:
            await message.answer("Нечего собирать")
            await message.answer()
    else:
        await message.answer("Вам не хватает места в амбаре")
        await message.answer()