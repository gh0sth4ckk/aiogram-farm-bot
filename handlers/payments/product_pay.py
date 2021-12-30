from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp

from payments.shipping_methods import EXAMPLE_SHIPPING
from payments.items.example_item import example_item


@dp.message_handler(Command("invoice"))
async def register_payment(message: types.Message):
    await dp.bot.send_invoice(message.from_user.id, **example_item.gen_invoice(), payload=123)
