from datetime import datetime

now_time = datetime.now()
ALL_YEARS = [i for i in range(1940, now_time.year+1)]
ALL_YEARS.reverse()

ALL_MONTH = [
    'January', 'February', 'March',
    'April', 'May', 'June', 'July',
    'August', 'September', 'October',
    'November', 'December']

ALL_MONTH_DICT = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12}

ALL_DAYS = [i for i in range(1, 32)]

ALL_RECORDS = []
