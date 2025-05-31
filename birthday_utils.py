from datetime import date

# 🧠 Зберігаємо попередній стан іменинників (опціонально можна зберігати у файл)
previous_birthdays = []

def filter_this_month(birthdays):
    """
    🔍 Повертає список іменинників поточного місяця.
    Використовується для надсилання сповіщень на початку кожного місяця.
    """
    today = date.today()
    return [b for b in birthdays if b['date'].month == today.month]

def detect_new_birthdays(current_birthdays):
    """
    🆕 Повертає список нових іменинників, які зʼявилися з моменту попереднього запуску.
    Порівнює з попереднім збереженим списком (у памʼяті).
    """
    global previous_birthdays
    new = [b for b in current_birthdays if b not in previous_birthdays]
    previous_birthdays = current_birthdays  # оновлюємо попередній стан
    return new