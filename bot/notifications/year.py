from bot.config import *


def year_notification_text(current_fires: int,
                           current_area: float,
                           extinguished_fires: int,
                           extinguished_area: float,
                           ):
    return f"""Всего по округу с начала года ликвидировано пожаров: {extinguished_fires} шт., площадь ликвидации, покрытая лесом составила {extinguished_area} га. Действует {current_fires} пожара площадью {current_area} га."""
