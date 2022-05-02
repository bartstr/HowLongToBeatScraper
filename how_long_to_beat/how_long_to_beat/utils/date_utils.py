from datetime import datetime
import re


def check_if_date_is_fully_valid(string):
    x = re.match('^\d+', string)
    if x is None:
        return True
    return False


def convert_string_date_to_date_object(string):
    return datetime.strptime(string, '%B %d, %Y').date()


def compare_full_dates(*args):
    main_l = []
    for x in args:
        d = convert_string_date_to_date_object(x)
        main_l.append(d)
    main_l.sort()
    return main_l[0]


def compare_year_only_dates(*args):
    years = list(args)
    years.sort()
    return int(years[0])

test_list = ['March 24, 1984', '1992', 'February 12, 1981']


def release_date_normalisation(self, data_list):
    """
    na stronie mamy podawane trzy rozne daty wydania (maksymalnie) EU US i JP
    na ogol w formacie MIESIAC_SLOWNIE DZIEN, ROK
    przyklad na gre nie wydana w US + na to, ze czasem data to jest sam ROK
    https://howlongtobeat.com/game?id=9876

    co trzeba zrobic:
    pobrac jak najwiecej tych dat, sprawdzic czy sa pelne, uwzglednic tylko pelne, zapisac wczesniejsza
    """

