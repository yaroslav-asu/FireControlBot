from bot.config import *
from parse_data import load_fire_data
import datetime


def month_notification_text(fires_count: int,
                            sum_area: float,
                            current_fires: int,
                            current_area: float,
                            extinguished_fires: int,
                            current_extinguished: int,
                            current_extinguished_area: float,
                            date,
                            time,
                            ):
    return f"""Возникло пожаров за этот месяц: {fires_count} шт., площадью {sum_area} га. Ликвидировано пожаров: {extinguished_fires} шт., Действует пожаров: {current_fires} шт., площадью {current_area} га, из них локализовано {current_extinguished} шт., площадью {current_extinguished_area} га. {date} {time}"""


def season_notification_text(
        fires_count,
        fires_area,
        current_fires,
        current_area: float,
):
    return f"""Всего по округу с начала пожароопасного сезона ликвидировано пожаров: {fires_count} шт., площадь ликвидации, покрытая лесом составила {fires_area} га. Действует {current_fires} пожара площадью {current_area} га."""


def year_notification_text(current_fires: int,
                           current_area: float,
                           extinguished_fires: int,
                           extinguished_area: float,
                           ):
    return f"""Всего по округу с начала года ликвидировано пожаров: {extinguished_fires} шт., площадь ликвидации, покрытая лесом составила {extinguished_area} га. Действует {current_fires} пожара площадью {current_area} га."""


def now_fires_notification_text(number, place, area, date, time, duration, cause):
    return f"Лесной пожар {number} {place}, площадь {area} га. Действует: {date} {time}. Продолжительность горения: {duration} час. {duration} мин. Причина возникновения: {cause}."


def now_localized_notification_text(number, place, area, date, time, duration, cause):
    return f"Лесной пожар {number} {place}, площадь {area} га. Локализован: {date} {time}. Продолжительность горения: {duration} час. {duration} мин. Причина возникновения: {cause}."


def now_extinguished_notification_text(number, place, area, date, time, duration, cause):
    return f"Лесной пожар {number} {place}, площадь {area} га. Действует: {date} {time}Локализован: {date} {time}. Продолжительность горения: {duration} час. {duration} мин. Причина возникновения: {cause}."


def get_summary_of_the_time(days: int):
    data = load_fire_data([("bot/extra_data/yasen_06_2022_getFireInformationResponse.json",
                           "bot/extra_data/yasen_06_2022_getDynamicsResponse.json"),
                          ("bot/extra_data/yasen_07_2022_getFireInformationResponse.json",
                           "bot/extra_data/yasen_07_2022_getDynamicsResponse.json")])
    fires_count = 0
    sum_area = 0
    for _, value in data.items():
        if value['date_start'] is None:
            continue
        if (datetime.datetime.now() - value['date_start']) < datetime.timedelta(days=days):
            fires_count += 1
            if value['area'] is not None:
                sum_area += value['area']
    return fires_count, sum_area


def get_summary_of_the_day():
    fires_count, sum_area = get_summary_of_the_time(1)
    return f'Возникло пожаров за последние сутки: {fires_count} шт., площадью {sum_area} га.'

def get_summary_of_the_season():
    fires_count, sum_area = get_summary_of_the_time(90)
    return f'Возникло пожаров за последнюю неделю: {fires_count} шт., площадью {sum_area} га.'

def get_summary_of_the_month():
    fires_count, sum_area = get_summary_of_the_time(30)
    return f'Возникло пожаров за последний месяц: {fires_count} шт., площадью {sum_area} га.'

def get_summary_of_the_year():
    fires_count, sum_area = get_summary_of_the_time(365)
    return f'Возникло пожаров за последний год: {fires_count} шт., площадью {sum_area} га.'
