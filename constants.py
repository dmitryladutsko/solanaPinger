import os

from dotenv import load_dotenv, find_dotenv

import logging


if load_dotenv(find_dotenv()):
    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SMTP_PORT = os.getenv("SMTP_PORT")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
    GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
else:
    logging.error(".env file NOT FOUNT")

BASE_URL = "https://api.binance.com/api/v3"
CURRENCY = 'SOLUSD'
SLEEP_TIME = 30

SMTP_SERVER = "smtp.gmail.com"
EMAIL_SUBJECT = "Test Email"
EMAIL_BODY = "Here are the latest metrics:\n"
