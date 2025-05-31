import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEET_NAME
import datetime
import os


# Область доступу до Google Sheets API
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(BASE_DIR, 'credentials.json')  # Цей файл  завантажуэмо з Google Cloud

def get_birthdays_from_sheet():
    # Авторизація через OAuth2
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)

    # Відкриваємо таблицю (за назвою з config.py) і читаємо дані з першого листа
    sheet = client.open_by_key(GOOGLE_SHEET_NAME).sheet1
    records = sheet.get_all_records()

    birthdays = []

    for record in records:
        name = record.get('ПІП') or record.get('ПІБ') or record.get('Name')
        date_str = record.get('Дата народження') or record.get('Date') or record.get('Birthday')
        if name and date_str:
            try:
                # Конвертація формату дати (наприклад: 15.06.1990)
                date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
                birthdays.append({'name': name, 'date': date})
            except ValueError:
                print(f'⚠️ Некоректна дата: {date_str} для {name}')
    return birthdays