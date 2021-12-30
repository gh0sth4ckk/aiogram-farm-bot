from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

shop_callback = CallbackData("shop", "shop_type")
houses_callback = CallbackData("house_shop", "house_type")
animals_callback = CallbackData("animals_shop", "animal")

shop_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text="Дома", callback_data=shop_callback.new("houses")),
        InlineKeyboardButton(text="Животные", callback_data=shop_callback.new("animals"))
    ]
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