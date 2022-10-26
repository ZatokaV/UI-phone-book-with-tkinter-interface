from datetime import datetime
from constants import ALL_MONTH_DICT


def vallide_bday(day, month, year):
    try:
        datetime_obj = datetime(
            year=int(year), month=ALL_MONTH_DICT[month], day=int(day))
        return datetime_obj
    except ValueError:
        return False


def correct_phone(phone):
    if " " in phone:
        new_phone = phone.replace(' ', '-')
        return new_phone
    return phone
