from telebot import types
from bot.config import *
from bot.interfaces.menues.main import show_main_menu


def handle_fires_statistic_period(message):
    if message.text == 'За день':
        pass
    elif message.text == 'За месяц':
        pass
    elif message.text == 'За год':
        pass
    elif message.text == 'За пажароопасный сезон':
        pass
    elif message.text == 'Назад':
        show_main_menu(message)


def show_fires_statistic_period_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("За день", "За месяц", "За год")
    markup.add("За пожароопасный сезон")
    markup.add("Назад")
    bot.send_message(message.chat.id, 'За какое время вы хотите узнать о пожарах?', reply_markup=markup)
    bot.register_next_step_handler(message, handle_fires_statistic_period)


