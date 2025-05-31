# Імпортуємо необхідні компоненти з бібліотеки python-telegram-bot
from telegram.ext import ApplicationBuilder, CommandHandler

# Імпортуємо функції-обробники
from telegram_bot import start, list_birthdays  # 🆕 додано list_birthdays

# Імпортуємо токен з конфігураційного файлу
from config import TELEGRAM_TOKEN

# Створюємо екземпляр Telegram-застосунку з токеном
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Додаємо обробник на команду /start
app.add_handler(CommandHandler("start", start))

# 🆕 Додаємо обробник на команду /list
app.add_handler(CommandHandler("list", list_birthdays))

# Основна точка входу — запускає бота в режимі "слухача"
if __name__ == '__main__':
    print('🤖 Бот слухає. Напишіть /start або /list...')
    app.run_polling()