from datetime import date, datetime

DATE_FORMAT = "%Y-%m-%d"


def subtract_days_from_dates(greater_date: date, minor_date: date) -> int:
    return (greater_date - minor_date).days


def str_to_date(date_str: str | date) -> date:
    if isinstance(date_str, date):
        return date_str
    return datetime.strptime(date_str, DATE_FORMAT).date()
