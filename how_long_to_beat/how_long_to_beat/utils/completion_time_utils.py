import re


def fraction_normalisation(string):
    number_of_hours_list = re.findall('\d+', string)
    number = float(number_of_hours_list[0])
    if '½' in string:
        number = number + 0.5
    return number

a = fraction_normalisation('23½')
b = fraction_normalisation('23')