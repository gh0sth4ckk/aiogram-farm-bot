from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData

fair_callback = CallbackData("fair", "product")

fair_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Продать шерсть", callback_data=fair_callback.new("wool"))],
    [InlineKeyboardButton(text="Продать яйца", callback_data=fair_callback.new("eggs"))],
    [InlineKeyboardButton(text="Продать молоко", callback_data=fair_callback.new("milk"))]
])