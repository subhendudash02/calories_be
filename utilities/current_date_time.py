from datetime import datetime

def get_current_date():
    return datetime.date(datetime.now())

def get_current_time():
    return datetime.time(datetime.now())
