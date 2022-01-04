from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

shop_callback = CallbackData("shop", "shop_type")
wood_callback = CallbackData("wood_shop", "wood")
barn_callback = CallbackData("barn_shop", "barn")
houses_callback = CallbackData("house_shop", "house_type")
animals_callback = CallbackData("animals_shop", "animal")

shop_keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text="🏠 Дома", callback_data=shop_callback.new("houses")),
        InlineKeyboardButton(text="🐶 Животные", callback_data=shop_callback.new("animals"))
    ],
    [InlineKeyboardButton(text="🪵 Купить доски", callback_data=shop_callback.new("wood"))],
    [InlineKeyboardButton(text="📦 Купить место в амбаре", callback_data=shop_callback.new("barn"))]
])

wood_shop_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Купить", callback_data=wood_callback.new("wood"))]
])

barn_shop_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Купить", callback_data=barn_callback.new("barn"))]
])

house_shop_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text="« 1 »", callback_data=houses_callback.new("chicken_coop")),
        InlineKeyboardButton(text="« 2 »", callback_data=houses_callback.new("cowshed"))
    ]
])

animals_shop_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text="« 1 »", callback_data=animals_callback.new("sheep")),
        InlineKeyboardButton(text="« 2 »", callback_data=animals_callback.new("chicken")),
        InlineKeyboardButton(text="« 3 »", callback_data=animals_callback.new("cow"))
    ]
])