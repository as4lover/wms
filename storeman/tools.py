from datetime import *
import pytz


au_timezone = pytz.timezone("Australia/Sydney")

today = datetime.now(au_timezone)


def get_last_friday():
    current_time = datetime.now(au_timezone)
    last_friday = (
        current_time.date()
        - timedelta(days=current_time.weekday())
        + timedelta(days=4, weeks=-1)
    )
    return last_friday


def get_last_monday():
    current_time = datetime.now(au_timezone)
    last_monday = (
        current_time.date()
        - timedelta(days=current_time.weekday())
        + timedelta(days=0, weeks=-1)
    )
    return last_monday


def get_this_monday():
    current_time = datetime.now(au_timezone)
    this_monday = (
        current_time.date()
        - timedelta(days=current_time.weekday())
        + timedelta(days=0, weeks=0)
    )
    return this_monday


def get_this_friday():
    current_time = datetime.now(au_timezone)
    this_friday = (
        current_time.date()
        - timedelta(days=current_time.weekday())
        + timedelta(days=4, weeks=0)
    )
    return this_friday


def get_this_month_start():
    start_date = today.replace(day=1)
    return start_date


def get_this_month_end():
    next_month = today.replace(day=28) + timedelta(days=4)
    res = next_month - timedelta(days=next_month.day)
    return res


def get_last_month_start():
    end_date = today.replace(day=1) - timedelta(days=1)
    first_date = end_date.replace(day=1)
    return first_date


def get_last_month_end():
    end_date = today.replace(day=1) - timedelta(days=1)
    return end_date
