from datetime import datetime
import re


def check_if_date_is_fully_valid(string):
    x = re.match('^\d+', string)
    if x is None:
        return True
    return False


def convert_string_date_to_date_object(string):
    try:
        return datetime.strptime(string, '%B %d, %Y').date()
    except ValueError:
        return None


def release_date_normalisation(date_list):
    """
    I assume that full date (with day and month, not year only) is more viable for data (which need to be considered in
    future. That's why this function is prioritizing full date over year only, and first check if in date_list is any
    full date if yes, it compares them, if no checks for year only dates, and compares them. If theres full date or
    year only date I prefer to have None returned.
    """
    years_only = []
    full_dates = []
    for x in date_list:
        is_valid = check_if_date_is_fully_valid(x)
        if is_valid:
            a = convert_string_date_to_date_object(x)
            full_dates.append(a)
        else:
            years_only.append(x)
    if full_dates:
        full_dates.sort()
        return full_dates[0]
    elif years_only:
        years_only.sort()
        return years_only[0]
    else:
        return None
