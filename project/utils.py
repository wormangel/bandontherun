from datetime import datetime

def mount_date(date, time):
    return datetime(date.year, date.month, date.day, hour=time.hour, minute=time.minute, second=time.second)