from bot.config import *
from telebot import types
import bot.notifications.texts as texts

@bot.inline_handler(lambda query: query.query == 'день')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Статистика', types.InputTextMessageContent(texts.get_summary_of_the_day()))
        r2 = types.InlineQueryResultArticle('2', 'Пожары за день', types.InputTextMessageContent(texts.get_summary_of_the_day()))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)
