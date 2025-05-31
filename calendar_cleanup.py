from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import GOOGLE_CALENDAR_ID


SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def delete_birthday_events():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    print('🔍 Отримую всі події з календаря...')
    page_token = None
    deleted_ids = set()
    count_deleted = 0

    while True:
        events_result = service.events().list(
            calendarId=GOOGLE_CALENDAR_ID,
            pageToken=page_token,
            maxResults=2500,
            singleEvents=False
        ).execute()

        events = events_result.get('items', [])
        for event in events:
            title = event.get('summary', '')
            event_id = event.get('id')
            if title.startswith('🎂 День народження:') and event_id not in deleted_ids:
                try:
                    service.events().delete(calendarId=GOOGLE_CALENDAR_ID, eventId=event_id).execute()
                    deleted_ids.add(event_id)
                    count_deleted += 1
                    print(f'🗑️ Видалено: {title}')
                except Exception as e:
                    print(f'⚠️ Не вдалося видалити "{title}": {e}')

        page_token = events_result.get('nextPageToken')
        if not page_token:
            break

    print(f'\n✅ Усього видалено подій: {count_deleted}')

if __name__ == '__main__':
    delete_birthday_events()