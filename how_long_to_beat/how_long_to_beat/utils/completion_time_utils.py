import re


def fraction_normalisation(string):
    number_of_hours_list = re.findall(r'\d+', string)
    number = float(number_of_hours_list[0])
    if '½' in string:
        number = number + 0.5
    return number
