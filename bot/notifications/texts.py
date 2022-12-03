from bot.core.config import *
from bot.parse_data import load_fire_data
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
        if (datetime.datetime.now() - value['date_start']).total_seconds() < 0:
            continue
        if (datetime.datetime.now() - value['date_start']) < datetime.timedelta(days=days):
            fires_count += 1
            if value['area'] is not None:
                sum_area += value['area']
    return fires_count, round(sum_area, 2)


def get_active_fires_count():
    data = load_fire_data([("bot/extra_data/yasen_06_2022_getFireInformationResponse.json",
                            "bot/extra_data/yasen_06_2022_getDynamicsResponse.json"),
                           ("bot/extra_data/yasen_07_2022_getFireInformationResponse.json",
                            "bot/extra_data/yasen_07_2022_getDynamicsResponse.json")])
    fires_count = 0
    sum_area = 0
    for _, value in data.items():
        if value['date_start'] is None or value['date_finish'] is not None:
            continue
        if (datetime.datetime.now() - value['date_start']).total_seconds() < 0:
            continue
        if (datetime.datetime.now() - value['date_start']).total_seconds() > 0 > (
                datetime.datetime.now() - value['date_start']).total_seconds():
            fires_count += 1
            if value['area'] is not None:
                sum_area += value['area']
    return fires_count, round(sum_area, 2)


def get_summary_of_the_day():
    fires_count_start, sum_area_start = get_summary_of_the_time(1)
    fires_count_progress, sum_area_progress = get_active_fires_count()
    return f'Возникло пожаров за последние сутки: {fires_count_start} шт., площадью {sum_area_start} га.\n' \
           f'Действует пожаров: {fires_count_progress} площадью {sum_area_progress} га.\n' \
           f'{datetime.datetime.now().strftime("%d.%m.%Y")} {datetime.datetime.now().strftime("%H:%M")}'


def get_summary_of_the_season():
    fires_count, sum_area = get_summary_of_the_time(90)
    fires_count_progress, sum_area_progress = get_active_fires_count()
    return f'Возникло пожаров за последнюю неделю: {fires_count} шт., площадью {sum_area} га.' \
           f'Действует пожаров: {fires_count_progress} площадью {sum_area_progress} га.\n' \
           f'{datetime.datetime.now().strftime("%d.%m.%Y")} {datetime.datetime.now().strftime("%H:%M")}'


def get_summary_of_the_month():
    fires_count, sum_area = get_summary_of_the_time(30)
    fires_count_progress, sum_area_progress = get_active_fires_count()
    return f'Возникло пожаров за последний месяц: {fires_count} шт., площадью {sum_area} га.' \
           f'Действует пожаров: {fires_count_progress} площадью {sum_area_progress} га.\n' \
           f'{datetime.datetime.now().strftime("%d.%m.%Y")} {datetime.datetime.now().strftime("%H:%M")}'


def get_summary_of_the_year():
    fires_count, sum_area = get_summary_of_the_time(365)
    fires_count_progress, sum_area_progress = get_active_fires_count()
    return f'Возникло пожаров за последний год: {fires_count} шт., площадью {sum_area} га.' \
           f'Действует пожаров: {fires_count_progress} площадью {sum_area_progress} га.\n' \
           f'{datetime.datetime.now().strftime("%d.%m.%Y")} {datetime.datetime.now().strftime("%H:%M")}'


def get_change_state_fire(type: str, locality: str, area: int, state: str) -> str:
    return f'{type} {locality} площадь {area} {state}'


def send_day_notification(chat_id):
    bot.send_message(chat_id=chat_id, text=get_summary_of_the_day())


def send_season_notification(chat_id):
    bot.send_message(chat_id=chat_id, text=get_summary_of_the_season())


def send_month_notification(chat_id):
    bot.send_message(chat_id=chat_id, text=get_summary_of_the_month())


def send_year_notification(chat_id):
    bot.send_message(chat_id=chat_id, text=get_summary_of_the_year())


def fire_state_change_notification(chat_id):
    bot.send_message(chat_id=chat_id, text=get_change_state_fire)
