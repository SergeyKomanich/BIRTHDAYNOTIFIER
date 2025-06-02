# === TELEGRAM APP ===
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram_bot import start, list_birthdays
from config import TELEGRAM_TOKEN
from telegram_bot import start, list_birthdays, all_birthdays  # додано all_birthdays
from telegram_bot import handle_message
from telegram_bot import all_birthdays, handle_message
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters



# Ініціалізуємо Telegram-застосунок
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Додаємо обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("list", list_birthdays))
app.add_handler(CommandHandler("alllist", all_birthdays))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("alllist", all_birthdays))

# Запускаємо бота в режимі слухача
if __name__ == '__main__':
    print('🤖 Бот слухає. Напишіть /start, щоб підписатись...')
    app.run_polling()

# === MAIN SCRIPT ===
import asyncio

# 📥 Отримання іменинників з Google Таблиці
from google_sheets import get_birthdays_from_sheet

# 📅 Синхронізація з Google Календарем
from google_calendar import sync_birthdays_to_calendar

# 📤 Надсилання повідомлень у Telegram
from telegram_bot import send_monthly_birthdays, notify_updates

# 🛠️ Обробка іменинників
from birthday_utils import filter_this_month, detect_new_birthdays

# 🧾 Логування (щоб не дублювати події)
from logger import log_birthdays, was_logged


# 🔁 Основна асинхронна функція
async def main_async():
    # 1. Отримуємо всі дні народження з таблиці
    birthdays = get_birthdays_from_sheet()

    # 2. Знаходимо нових людей
    new_birthdays = detect_new_birthdays(birthdays)

    # 3. Фільтруємо лише тих, кого ще не додавали в календар
    birthdays_to_add = [
        b for b in new_birthdays
        if not was_logged(b['name'], b['date'], 'calendar')
    ]

    # 4. Додаємо нових людей у календар + повідомляємо в Telegram
    if birthdays_to_add:
        sync_birthdays_to_calendar(birthdays_to_add)
        log_birthdays(birthdays_to_add, 'calendar')
        await notify_updates(birthdays_to_add)

    # 5. Вибираємо іменинників поточного місяця
    this_month_birthdays = filter_this_month(birthdays)

    # 6. Надсилаємо тільки тим, кого ще не вітали цього місяця
    birthdays_to_notify = [
        b for b in this_month_birthdays
        if not was_logged(b['name'], b['date'], 'telegram')
    ]

    if birthdays_to_notify:
        await send_monthly_birthdays(birthdays_to_notify)
        log_birthdays(birthdays_to_notify, 'telegram')


# 🚀 Точка входу
if __name__ == '__main__':
    asyncio.run(main_async())