import json
import os
import asyncio
from telegram import Bot, Update
from telegram.ext import ContextTypes
from config import TELEGRAM_TOKEN
from subscribers_logger import log_subscriber
from google_sheets import get_birthdays_from_sheet
from birthday_utils import filter_this_month
from subscribers_logger import log_subscriber_to_csv

# Ініціалізуємо бота з токеном із .env
bot = Bot(token=TELEGRAM_TOKEN)

# Назва JSON-файлу, де зберігатимемо список підписників (chat_id)
CHAT_IDS_FILE = 'chat_ids.json'

# Завантажуємо chat_id користувачів, які вже підписались
def load_chat_ids() -> list[int]:
    if os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, 'r') as f:
            return json.load(f)
    return []

# Зберігаємо оновлений список chat_id у файл
def save_chat_ids(chat_ids: list[int]) -> None:
    with open(CHAT_IDS_FILE, 'w') as f:
        json.dump(chat_ids, f)

# Обробляємо команду /start — додає користувача до списку підписників
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    chat_ids = load_chat_ids()

    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        save_chat_ids(chat_ids)
        log_subscriber(chat_id, update.effective_user.username)
        log_subscriber_to_csv(chat_id, update.effective_user.username)

    await update.message.reply_text("👋 Привіт! Я бот-нагадувач про дні народження.\nНатисни /list, щоб побачити іменинників цього місяця.")

# Функція надсилання списку іменинників цього місяця всім підписникам
async def send_monthly_birthdays(birthdays: list[dict]) -> None:
    if not birthdays:
        return

    chat_ids = load_chat_ids()
    message = '🎉 Іменинники цього місяця:\n'
    for person in birthdays:
        message += f"- {person['name']} ({person['date'].strftime('%d.%m')})\n"

    for chat_id in chat_ids:
        await bot.send_message(chat_id=chat_id, text=message)

# Функція для сповіщення про нових іменинників
async def notify_updates(new_people: list[dict]) -> None:
    if not new_people:
        return

    chat_ids = load_chat_ids()
    message = '🔔 Додано нових іменинників:\n'
    for person in new_people:
        message += f"- {person['name']} ({person['date'].strftime('%d.%m')})\n"

    for chat_id in chat_ids:
        await bot.send_message(chat_id=chat_id, text=message)

# Обробник команди /list
async def list_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birthdays = get_birthdays_from_sheet()
    this_month = filter_this_month(birthdays)

    if not this_month:
        await update.message.reply_text('😕 Цього місяця немає іменинників.')
        return

    message = '📅 Іменинники цього місяця:\n'
    for person in this_month:
        message += f"- {person['name']} ({person['date'].strftime('%d.%m')})\n"

    await update.message.reply_text(message)