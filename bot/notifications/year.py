from bot.config import *


def year_notification(chat_id,
                      current_fires: int,
                      current_area: float,
                      extinguished_fires: int,
                      extinguished_area: float,
                      ):
    bot.send_message(chat_id,
                     f"""
                     Всего по округу с начала года ликвидировано пожаров: {extinguished_fires} шт., 
                     площадь ликвидации, покрытая лесом составила {extinguished_area} га. 
                     Действует {current_fires} пожара площадью {current_area} га.
                     """
                     )
