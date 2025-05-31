import json
import os
from datetime import datetime

LOG_FILE = 'birthday_log.json'

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def log_birthdays(persons, action):
    logs = load_logs()
    now = datetime.now().isoformat(timespec='seconds')

    for p in persons:
        logs.append({
            'name': p['name'],
            'date': p['date'].isoformat(),
            'action': action,
            'timestamp': now
        })

    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

def was_logged(name, date, action):
    logs = load_logs()
    for log in logs:
        if log['name'] == name and log['date'] == date.isoformat() and log['action'] == action:
            return True
    return False