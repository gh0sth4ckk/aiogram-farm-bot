from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

profile_callback = CallbackData("profile", "btn")

profile_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Ферма", callback_data=profile_callback.new("farm")), InlineKeyboardButton(text="Магазин", callback_data=profile_callback.new("shop"))],
    [InlineKeyboardButton(text="Донат", callback_data=profile_callback.new("donate"))]
])