from bot.config import *


def day_notification_text(chat_id,
                          fires_count: int,
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
