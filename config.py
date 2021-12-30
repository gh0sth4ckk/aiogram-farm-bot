"""
Configuration file.
"""
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PAY_TOKEN = str(os.getenv("PAYMENT_TOKEN"))
IP = str(os.getenv("IP"))
USE_REDIS = bool(os.getenv("USE_REDIS"))

admins = [
    520809126
]

# ================================ REDIS ================================

aiogram_redis = {
    'host': IP,
}

redis = {
    'address': (IP, 6379),
    'encoding': 'utf8'
}
