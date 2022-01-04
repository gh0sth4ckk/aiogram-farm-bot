from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

farm_keyboard = ReplyKeyboardMarkup([
    [KeyboardButton(text="🐑 Сад")],
    [KeyboardButton(text="🐄 Коровник"), KeyboardButton(text="🐓 Курятник")]
], resize_keyboard=True, one_time_keyboard=True)