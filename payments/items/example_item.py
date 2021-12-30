from aiogram.types.labeled_price import LabeledPrice
from payments.item import Product

example_item = Product(
    title="Тестовый товар",
    description="Описание",
    start_parameter="invoice_example",
    currency="RUB",
    prices=[LabeledPrice(label="Тестовый товар", amount=1000_0)],
    photo_url="https://site.ru/image.png"
)