from telebot import types
from bot.config import *
from bot.interfaces.menues.main import show_main_menu
from bot.notifications.texts import day_notification_text, month_notification_text, year_notification_text, season_notification_text


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
            bot.send_message(message.chat.id, day_notification_text(message.chat.id, 1, 1, 1, 1, 1, 1, 1, 1))
        elif message.text == 'За месяц':
            bot.send_message(message.chat.id, month_notification_text(message.chat.id, 1, 1, 1, 1, 1, 1, 1, 1))
        elif message.text == 'За год':
            bot.send_message(message.chat.id, year_notification_text(1, 1, 1, 1))
        elif message.text == 'За пожароопасный сезон':
            bot.send_message(message.chat.id, season_notification_text(1, 1, 1, 1))
        elif message.text == 'Назад':
            del data['fire_statistic_menu']
            show_main_menu(message)
