from telegram.ext import ApplicationBuilder, CommandHandler
from telegram_bot import start, list_birthdays
from config import TELEGRAM_TOKEN

# Ініціалізуємо Telegram-застосунок
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Додаємо обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("list", list_birthdays))

# Запускаємо бота в режимі слухача
if __name__ == '__main__':
    print('🤖 Бот слухає. Напишіть /start, щоб підписатись...')
    app.run_polling()