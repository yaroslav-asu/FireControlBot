from bot.config import *
from parse_data import load_fire_data
import datetime


def day_notification_text(fires_count: int,
                          sum_area: float,
                          current_fires: int,
                          current_area: float,
                          extinguished_fires: int,
                          extinguished_area: float,
                          date,
                          time,
                          ):
    return f"Возникло пожаров за последние сутки: {fires_count} шт., площадью {sum_area} га. " \
           f"Действует пожаров: {current_fires} шт., площадью {current_area} га, " \
           f"из них локализовано {extinguished_fires} шт., площадью {extinguished_area} га. " \
           f"{date} {time}"


def get_summary_of_the_day():
    data = load_fire_data([("bot/extra_data/yasen_06_2022_getFireInformationResponse.json",
                            "bot/extra_data/yasen_06_2022_getDynamicsResponse.json"),
                           ("bot/extra_data/yasen_07_2022_getFireInformationResponse.json",
                            "bot/extra_data/yasen_07_2022_getDynamicsResponse.json")])
    fires_count = 0
    sum_area = 0
    for _, value in data.items():
        if datetime.datetime.now() - value['date_start'] < datetime.timedelta(days=1):
            fires_count += 1
            sum_area += value['area']
    return f'Возникло пожаров за последние сутки: {fires_count} шт., площадью {sum_area} га.'
