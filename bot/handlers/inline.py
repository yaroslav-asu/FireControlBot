from bot.config import *
from telebot import types
from bot.notifications import day

@bot.inline_handler(lambda query: query.query == 'день')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Статистика', types.InputTextMessageContent(day.day_notification_text(1, 4, 12.4, 12, 40.3, 12, 40.3, '03.12.2022', '18.00')))
        r2 = types.InlineQueryResultArticle('2', 'Пожары за день', types.InputTextMessageContent(day.get_summary_of_the_day()))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)
