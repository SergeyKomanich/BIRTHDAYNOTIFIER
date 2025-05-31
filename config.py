import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME')
GOOGLE_CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CREDS_FILE = '/Users/serhii/birthday_notifier/credentials.json'