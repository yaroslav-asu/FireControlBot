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
