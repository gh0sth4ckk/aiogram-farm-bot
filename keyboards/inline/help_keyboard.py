from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

help_callback = CallbackData("help", "btn")

help_keyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text="Гайд", callback_data=help_callback.new("guide")),
        InlineKeyboardButton(text="Доступные команды", callback_data=help_callback.new("commands"))
    ]
])