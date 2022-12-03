from telebot import types
from bot.config import *
from bot.interfaces.menues.main import show_main_menu
from bot.notifications.day import day_notification
from bot.notifications.month import month_notification
from bot.notifications.season import season_notification
from bot.notifications.year import year_notification


def show_fires_statistic_period_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("За день", "За месяц", "За год")
    markup.add("За пожароопасный сезон")
    markup.add("Назад")
    bot.send_message(message.chat.id, 'За какое время вы хотите узнать о пожарах?', reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.fire_statistic_menu, message.chat.id)


@bot.message_handler(state=UserState.fire_statistic_menu)
def handle_fires_statistic_period(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fire_statistic_menu'] = message.text
         # TODO add data
        if message.text == 'За день':
            day_notification(message.chat.id, 1, 1, 1, 1, 1, 1, 1, 1)
        elif message.text == 'За месяц':
            month_notification(message.chat.id, 1, 1, 1, 1, 1, 1, 1, 1, 1)
        elif message.text == 'За год':
            year_notification(message.chat.id, 1, 1, 1, 1)
        elif message.text == 'За пажароопасный сезон':
            season_notification(message.chat.id, 1, 1, 1, 1)
        elif message.text == 'Назад':
            del data['fire_statistic_menu']
            show_main_menu(message)

