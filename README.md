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

# Оновлений

# BirthdayNotifier 🎈

📅 **Автоматичне нагадування про дні народження з Google Таблиці у Google Календар та Telegram.**

---

## ✅ Що вміє бот:

* Читати список днів народження з Google Таблиці
* Додавати їх у Google Календар
* Надсилати сповіщення в Telegram:

  * На початку кожного місяця
  * При додаванні нових записів
* Підтримка декількох користувачів Telegram
* Логування в CSV та JSON

---

## ⚙️ Налаштування проєкту

### 1. Клонування репозиторію

```bash
git clone https://github.com/SergeyKomanich/BIRTHDAYNOTIFIER.git
cd BIRTHDAYNOTIFIER
```

### 2. Встановлення віртуального середовища

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

### 4. Створення `.env` файлу

Створи файл `.env` з таким вмістом:

```
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id (необов'язково, використовується лише для одиночного надсилання)
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_CALENDAR_ID=your_calendar_id
```

### 5. Створення `credentials.json`

Завантаж із [Google Cloud Console](https://console.cloud.google.com/apis/credentials) ключ облікового запису (Service Account) для API доступу до Google Sheets + Calendar і збережи як:

```
credentials.json
```

---

## 🚀 Запуск

```bash
python main.py
```

---

## 🤝 Telegram-бот

### Команди:

```
/start - Підписатись на сповіщення
/list - Переглянути іменинників цього місяця
```

### Запуск бота окремо:

```bash
python telegram_listener.py
```

---

## ⏰ Автоматичний запуск (crontab)

Відкрий crontab:

```bash
crontab -e
```

Додай запуск на початку кожного місяця:

```
0 9 1 * * /full/path/to/venv/bin/python /full/path/to/main.py >> /full/path/to/cron_log.txt
```

---

## 📊 Логування

* `subscribers.csv` — лог підписників Telegram
* `chat_ids.json` — chat\_id користувачів
* `log_calendar.csv`, `log_telegram.csv` — лог надісланих подій

---

## 🌟 Автор

**Serhii Komanich**
Telegram: \[@yourusername]

---

## 📄 Ліцензія

MIT License
