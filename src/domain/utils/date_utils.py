from datetime import date, datetime
from typing import Optional

DATE_FORMATS = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"]


def subtract_days_from_dates(greater_date: date, minor_date: date) -> int:
    return (greater_date - minor_date).days


def str_to_date(date_str: str | date) -> Optional[date]:
    if isinstance(date_str, date):
        return date_str
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, date_format).date()
        except ValueError:
            pass
    return None
