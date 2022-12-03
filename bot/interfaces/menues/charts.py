from telebot import types
from bot.config import *
from bot.interfaces.menues.main import show_main_menu
from bot.utils import get_db
from bot.crud.crud_user import user

button_titles = {
    'count': ["Количество", False],
    'causes': ["Причины", False],
    'area': ["Площадь", False],
    'time': ["Среднее время", False],
}


def handle_select_fire_period(message):
    pass


def select_fires_period(message):
    pass


@bot.message_handler(state=UserState.select_chart_menu)
def handle_chart_select(message):
    if message.text == 'Назад':
        show_charts_menu(message, )


def select_chart_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Точечная")
    markup.add("Круговая")
    markup.add("Столбчатая")
    markup.add("Назад")
    bot.send_message(message.chat.id, "Веберите тип диараммы", reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.select_chart_menu, message.chat.id)


@bot.message_handler(state=UserState.charts_menu)
def handle_buttons_toggling(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['charts_menu'] = True
    if message.text == 'Назад':
        show_main_menu(message)
        return
    elif message.text == 'Далее':
        selected_at_least_one = False
        for key, values in button_titles.items():
            if values[1]:
                selected_at_least_one = True
        if not selected_at_least_one:
            show_charts_menu(message, 'Нужно выбрать что-то!')
        else:
            select_chart_menu(message)
        return
    for key, values in button_titles.items():
        if values[0] == message.text.replace(' ✅', ''):
            button_titles[key][1] = not button_titles[key][1]
    show_charts_menu(message, 'Еще что то?')


def show_charts_menu(message, text='Какие должны быть данные'):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['charts_menu'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    titles = [f"{button_titles[title][0]} {'✅' if button_titles[title][1] else ''}" for title in button_titles.keys()]
    markup.row(titles[0], titles[1])
    markup.row(titles[2], titles[3])
    markup.add("Далее")
    markup.add("Назад")
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.charts_menu, message.chat.id)
