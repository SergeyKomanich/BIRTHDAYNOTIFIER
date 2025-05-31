# 🎂 Birthday Notifier

Автоматичне додавання днів народження з Google Таблиці у Google Календар з Telegram-сповіщенням.

## 📌 Основний функціонал

- Читає дні народження з Google Таблиці
- Додає нових людей у Google Календар
- Надсилає щомісячні повідомлення про іменинників у Telegram
- Автоматично логує оброблені іменинники
- Зберігає підписників Telegram у `chat_ids.json`

## ⚙️ Команди

```bash
python main.py           # Запуск основного скрипта
python telegram_start.py # Запуск Telegram-бота для /start і /list
```

## 🔐 Файли конфігурації

- `.env` — зберігає конфіденційні ключі (TOKEN, CHAT_ID, etc.)
- `credentials.json` — ключ сервісного акаунта Google (для API)
- `chat_ids.json` — збережені підписники Telegram

## 🧱 Структура проекту

```
birthday_notifier/
├── main.py
├── telegram_start.py
├── telegram_bot.py
├── google_sheets.py
├── google_calendar.py
├── birthday_utils.py
├── logger.py
├── subscribers_logger.py
├── .env
├── credentials.json
├── chat_ids.json
└── README.md
```

## 🔧 Залежності

Встанови залежності через pip:

```bash
pip install -r requirements.txt
```
