import csv
from datetime import datetime
import os

CSV_FILE = 'subscribers.csv'

# Додає нового підписника, якщо ще не збережено
def log_subscriber(chat_id, username):
    # Якщо CSV ще не існує — створимо з заголовком
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['chat_id', 'username', 'joined_at'])

    # Перевіряємо, чи підписник уже записаний
    with open(CSV_FILE, mode='r') as f:
        existing_ids = [row[0] for row in csv.reader(f)][1:]  # пропускаємо заголовок

    if str(chat_id) not in existing_ids:
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([chat_id, username or 'unknown', datetime.now().isoformat()])