
import json
import os
import asyncio
from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from config import TELEGRAM_TOKEN
from subscribers_logger import log_subscriber
from google_sheets import get_birthdays_from_sheet
from birthday_utils import filter_this_month
from birthday_utils import detect_new_birthdays

# Ініціалізуємо бота
bot = Bot(token=TELEGRAM_TOKEN)

# Файл для зберігання chat_id підписників
CHAT_IDS_FILE = 'chat_ids.json'

# Завантаження chat_id
def load_chat_ids() -> list[int]:
    if os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, 'r') as f:
            return json.load(f)
    return []

# Збереження chat_id
def save_chat_ids(chat_ids: list[int]) -> None:
    with open(CHAT_IDS_FILE, 'w') as f:
        json.dump(chat_ids, f)

# 📲 Клавіатура
def get_main_keyboard():
    keyboard = [
        [KeyboardButton('📅 Поточний місяць')],
        [KeyboardButton('📋 Повний список')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start — підписка
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    chat_ids = load_chat_ids()

    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        save_chat_ids(chat_ids)
        log_subscriber(chat_id, update.effective_user.username)

    await update.message.reply_text(
        "👋 Привіт! Я бот-нагадувач про дні народження."
        "Використай меню нижче або команди /list /alllist:",
        reply_markup=get_main_keyboard()
    )

# /list — іменинники поточного місяця
async def list_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birthdays = get_birthdays_from_sheet()
    this_month = filter_this_month(birthdays)

    if not this_month:
        await update.message.reply_text('😕 Цього місяця немає іменинників.')
        return

    message = '📅 Іменинники цього місяця:'
    for person in this_month:
        message += f"- {person['name']} ({person['date'].strftime('%d.%m')})\n"

    await update.message.reply_text(message)

# /alllist — усі іменинники
async def all_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    birthdays = get_birthdays_from_sheet()
    if not birthdays:
        await update.message.reply_text('🤷 Немає іменинників у списку.')
        return

    message = '📋 Повний список іменинників:'
    for person in birthdays:
        message += f"- {person['name']} ({person['date'].strftime('%d.%m')})\n"

    await update.message.reply_text(message)

# Обробка натискань кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == '📅 Поточний місяць':
        await list_birthdays(update, context)
    elif text == '📋 Повний список':
        await all_birthdays(update, context)
    else:
        await update.message.reply_text('🤖 Я не впізнав цю команду. Спробуй ще раз.')

# 🔔 Сповіщення про нових
async def notify_updates(new_people: list[dict]) -> None:
    if not new_people:
        return

    chat_ids = load_chat_ids()
    message = '🔔 Додано нових іменинників:\n'
    for person in new_people:
        message += f"- {person['name']} ({person['date'].strftime('%d.%m')})\n"

    for chat_id in chat_ids:
        await bot.send_message(chat_id=chat_id, text=message)

# 🎉 Сповіщення про поточний місяць
async def send_monthly_birthdays(birthdays: list[dict]) -> None:
    if not birthdays:
        return

    chat_ids = load_chat_ids()
    message = '🎉 Іменинники цього місяця:\n'
    for person in birthdays:
        message += f"- {person['name']} ({person['date'].strftime('%d.%m')})\n"

    for chat_id in chat_ids:
        await bot.send_message(chat_id=chat_id, text=message)
