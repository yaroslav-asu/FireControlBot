from bot.config import *


def season_notification(chat_id,
                        fires_count,
                        fires_area,
                        current_fires,
                        current_area: float,
                        ):
    bot.send_message(chat_id,
                     f"""
                     Всего по округу с начала пожароопасного сезона ликвидировано пожаров: {fires_count} шт., 
                     площадь ликвидации, покрытая лесом составила {fires_area} га. 
                     Действует {current_fires} пожара площадью {current_area} га.
                     """
                     )
