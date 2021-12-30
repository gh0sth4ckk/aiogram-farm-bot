"""
Экземпляр предмета продажи.
"""
from dataclasses import dataclass
from typing import List

from aiogram.types import LabeledPrice

from config import PAY_TOKEN

@dataclass
class Product:
    """Класс экземпляра будушего товара"""
    title: str                      # Название товара
    description: str                # Описание товара
    start_parameter: str            # Начальный параметр
    currency: str                   # Валюта, указывается в стандарте ISO4217
    prices: List["LabeledPrice"]    # Цена
    provider_data: dict = None      # 
    photo_url: str = None           # Ссылка на фото
    photo_size: int = 600           # Размер фото
    need_name: bool = False         # Требуется ли имя покупателя
    need_phone_number: bool = False # Требуется ли номер покупателя
    need_email: bool = False        # Требуется ли Email покупателя
    need_shipping_address: bool = False # Требуется ли адрес доставки покупателя
    is_flexible: bool = False       # Будет ли изменена цена при изменении способа оплаты

    provider_token: str = PAY_TOKEN # Токен который выдает платежный сервис

    def gen_invoice(self) -> dict:
        """Возвращает этот объект ввиде словаря, который в последсвии
        можно будет преобразовать в аргументы для функции"""
        return self.__dict__