import csv
import os
import logging
from datetime import datetime

# CSV-файл для логування іменинників
LOG_FILE = 'log.csv'

# Створення каталогу logs для централізованих логів
if not os.path.exists('logs'):
    os.makedirs('logs')

# Налаштування logging
logging.basicConfig(
    filename='logs/birthday_notifier.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Централізоване логування
def log_event(message: str):
    logging.info(message)

# Перевірка, чи вже логувався цей запис
def was_logged(name, date, target):
    if not os.path.exists(LOG_FILE):
        return False
    with open(LOG_FILE, mode='r') as f:
        for row in csv.reader(f):
            if row == [name, str(date), target]:
                return True
    return False

# Додає новий запис до логів у CSV
def log_birthdays(birthdays, target):
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        for person in birthdays:
            writer.writerow([person['name'], person['date'], target])
            log_event(f'Logged {person["name"]} ({person["date"]}) for {target}')