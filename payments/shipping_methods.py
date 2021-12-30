"""
Методы доставки используемые при платежах
"""
from aiogram.types import ShippingOption
from aiogram.types import LabeledPrice


EXAMPLE_SHIPPING = ShippingOption(
    id="Идентификатор",
    title="Название метода доставки",
    prices=[
        LabeledPrice("Название метода", 1000_0)
    ]
)