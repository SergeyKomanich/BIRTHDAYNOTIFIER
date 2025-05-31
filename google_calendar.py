from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import GOOGLE_CALENDAR_ID
import datetime

# Шлях до service account credentials
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def sync_birthdays_to_calendar(birthdays):
    # Авторизація
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    for person in birthdays:
        event = {
            'summary': f"🎂 День народження: {person['name']}",
            'start': {
                'date': person['date'].isoformat(),
                'timeZone': 'Europe/Kyiv'
            },
            'end': {
                'date': (person['date'] + datetime.timedelta(days=1)).isoformat(),
                'timeZone': 'Europe/Kyiv'
            },
            'recurrence': ['RRULE:FREQ=YEARLY'],
            'reminders': {
                'useDefault': True
            }
        }

        try:
            service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event).execute()
            print(f"✅ Додано до календаря: {person['name']}")
        except Exception as e:
            print(f"❌ Помилка при додаванні {person['name']}: {e}")