from bot.config import *


def season_notification_text(
        fires_count,
        fires_area,
        current_fires,
        current_area: float,
):
    return f"""Всего по округу с начала пожароопасного сезона ликвидировано пожаров: {fires_count} шт., площадь ликвидации, покрытая лесом составила {fires_area} га. Действует {current_fires} пожара площадью {current_area} га."""
