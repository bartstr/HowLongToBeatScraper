from datetime import datetime
import re


def check_if_date_is_fully_valid(string):
    if ',' not in string:
        x = re.match(r'^\d+', string)
        if x is None:
            return 'month_year'
        else:
            return 'year_only'
    else:
        return 'full_date'


def convert_full_date_string_to_date_object(string):
    try:
        return datetime.strptime(string, '%B %d, %Y').date()
    except ValueError:
        return None


def convert_month_and_year_date_string_to_date_object(string):
    try:
        return datetime.strptime(string, '%B %Y').date()
    except ValueError:
        return None


def release_date_normalisation(date_list):
    """
    I assume that full date (with day, month and year, not month and year or year only) is more viable for data
    (which need to be considered in future.
    That's why this function is prioritizing full date over year only, and first check if in date_list is any
    full date if yes, it compares them, if no checks for year only dates, and compares them. If theres full date or
    year only date I prefer to have None returned.
    """
    years_only = []
    month_year = []
    full_dates = []
    for x in date_list:
        string_contains = check_if_date_is_fully_valid(x)
        if string_contains == 'full_date':
            a = convert_full_date_string_to_date_object(x)
            full_dates.append(a)
        elif string_contains == 'month_year':
            a = convert_month_and_year_date_string_to_date_object(x)
            month_year.append(a)
        else:
            years_only.append(x)
    if full_dates:
        full_dates.sort()
        return full_dates[0]
    elif month_year:
        month_year.sort()
        return month_year[0]
    elif years_only:
        years_only.sort()
        return years_only[0]
    else:
        return None
