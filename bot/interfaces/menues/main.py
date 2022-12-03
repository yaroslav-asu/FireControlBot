from telebot import types
from bot.core.config import *


def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_titles = ["Узнать о пожарах 🔥", "Посмотреть графики 🗠"]
    for title in button_titles:
        markup.add(title)
    bot.send_message(message.chat.id, 'Выберите то, о чем вы хотите узнать', reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.main_menu, message.chat.id)


@bot.message_handler(state=UserState.main_menu)
def handle_main_menu_select(message):
    from bot.interfaces.menues.charts import show_charts_menu
    from bot.interfaces.menues.fire_dates import show_fires_statistic_period_menu
    if message.text == 'Узнать о пожарах 🔥':
        show_fires_statistic_period_menu(message)
    elif message.text == 'Посмотреть графики 🗠':
        show_charts_menu(message)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['main_menu'] = message.text
