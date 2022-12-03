from bot.config import *
from bot.functions.help import show_help

from bot.notifications.texts import get_summary_of_the_day


# greeting handler functions
@bot.message_handler(state="*", commands=['help'])
def handle_help(message):
    show_help(message)


# TODO change functions code
@bot.message_handler(state="*", commands=['get_current_fires'])
def handle_help(message):
    bot.send_message(message.chat.id, get_summary_of_the_day())


@bot.message_handler(state="*", commands=['get_day_info'])
def handle_help(message):
    bot.send_message(message.chat.id, get_summary_of_the_day())


@bot.message_handler(state="*", commands=['get_month_info'])
def handle_help(message):
    bot.send_message(message.chat.id, get_summary_of_the_day())


@bot.message_handler(state="*", commands=['get_year_info'])
def handle_help(message):
    bot.send_message(message.chat.id, get_summary_of_the_day())


@bot.message_handler(state="*", commands=['get_season_info'])
def handle_help(message):
    bot.send_message(message.chat.id, get_summary_of_the_day())


@bot.message_handler(state="*", commands=['get_chart'])
def handle_help(message):
    params = message.text.split(' ')[1:]
    types = {
        'круговая': 'pie',
        'прямые': 'line',
        'столбцы': 'bar',
    }
    data = {
        'количество': 'count',
        'причины': 'reasons',
        'площадь': 'area',
        'среднее время': 'time',
    }
    try:
        type = types[params[0]]
        dates = params[-2:]
        data = list(map(lambda x: data[x], params[1:-2]))
        print(type, data, dates)
    except (KeyError, IndexError):
        bot.send_message(message.chat.id, 'Неверный формат запроса, попробуйте еще раз')
