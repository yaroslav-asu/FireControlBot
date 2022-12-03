from bot.config import *


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
