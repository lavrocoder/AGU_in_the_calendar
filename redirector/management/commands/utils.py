import calendar
from datetime import datetime


def get_first_day_of_current_month_and_last_day_of_next_month():
    """
    Функция, возвращающая кортеж из двух дат: первое число текущего месяца и последнее число следующего месяца.
    :return:
    """
    now = datetime.now()  # получаем текущую дату и время
    next_month = now.month + 1 if now.month != 12 else 1  # вычисляем номер следующего месяца
    year = now.year + 1 if next_month == 1 else now.year  # вычисляем год следующего месяца
    last_day_next_month = calendar.monthrange(year, next_month)[1]  # получаем последнее число следующего месяца
    first_day = datetime(now.year, now.month, 1)  # создаем новую дату с первым числом текущего месяца
    last_day = datetime(year, next_month, last_day_next_month, 23, 59, 59)  # дата с последним число следующего месяца
    return first_day, last_day
