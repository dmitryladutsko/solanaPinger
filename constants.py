import logging
import os

from dotenv import load_dotenv, find_dotenv

if load_dotenv(find_dotenv()):
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHATS = os.getenv("CHATS")
else:
    logging.error(".env file NOT FOUNT")

BASE_URL = "https://api.binance.com/api/v3"
CURRENCY = 'SOLUSDT'
SLEEP_TIME = 30
