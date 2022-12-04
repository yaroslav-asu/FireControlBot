from datetime import datetime

from telebot import types
from bot.core.config import *
from bot.heatmap.heatmap_generator import show_heat_map
from bot.interfaces.menues.main import show_main_menu
from telebot.types import ReplyKeyboardRemove
from bot.plot_preparing.prepare_plots import build_linear_plot, build_pie_chart

button_titles = {
    'count': ["Количество", False],
    'causes': ["Причины", False],
    'area': ["Площадь", False],
    'time': ["Среднее время", False],
}


@bot.message_handler(state=UserState.chart_type)
def handle_select_fire_period(message):
    if message.text == "⬅️ Назад":
        show_select_chart_menu(message)
        return
    try:
        first_date, second_date = message.text.split()
        first_date = datetime.strptime(first_date, "%d.%m.%Y")
        second_date = datetime.strptime(second_date, "%d.%m.%Y")
        bot.send_message(message.chat.id,
                         "Отлично, осталось только подождать, пока загрузятся диаграммы")
        bot.set_state(message.from_user.id, UserState.select_fires_period, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            match data["chart_type"]:
                case "Линейная":
                    img = build_linear_plot(data["chart_data"], first_date, second_date)
                case "Круговая":
                    img = build_pie_chart(data["chart_data"], first_date, second_date)
            bot.send_photo(message.from_user.id, img)
            show_main_menu(message)
    except Exception as e:
        # first_date, second_date = message.text.split(' - ')
        # first_date = datetime.strptime(first_date, "%d.%m.%Y")
        # second_date = datetime.strptime(second_date, "%d.%m.%Y")
        # print(first_date, second_date)
        bot.send_message(message.chat.id,
                         "Что-то пошло не так, попробуйте еще раз")
        print(e)


@bot.message_handler(state=UserState.select_chart_menu)
def handle_chart_select(message):
    if message.text == '⬅️ Назад':
        show_charts_menu(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("⬅️ Назад")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['chart_type'] = message.text[2:]
        bot.send_message(message.chat.id,
                         "Введите даты через пробел: дд.мм.гггг дд.мм.гггг",
                         reply_markup=markup)
        bot.set_state(message.from_user.id, UserState.chart_type, message.chat.id)


def show_select_chart_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📈 Линейная")
    markup.add("🍕 Круговая")
    markup.add("⬅️ Назад")
    bot.send_message(message.chat.id, "Веберите тип диараммы", reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.select_chart_menu, message.chat.id)


@bot.message_handler(state=UserState.charts_menu)
def handle_buttons_toggling(message):
    message_text = message.text.replace(' ✅', '')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['charts_menu'] = True
    if message.text == '⬅️ Назад':
        show_main_menu(message)
        return
    elif message.text == 'Далее ➡️':
        selected_at_least_one = False
        for key, values in button_titles.items():
            if values[1]:
                selected_at_least_one = True
        if not selected_at_least_one:
            show_charts_menu(message, 'Нужно обязательно что-то выбрать!')
        else:
            show_select_chart_menu(message)
        return
    for key, values in button_titles.items():
        if values[0] == message_text:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                if 'chart_data' not in data.keys():
                    data['chart_data'] = {message_text, }
                else:
                    if message_text in data['chart_data']:
                        data['chart_data'].remove(message_text)
                    else:
                        data['chart_data'].add(message_text)
            button_titles[key][1] = not button_titles[key][1]
    show_charts_menu(message, 'Еще что то?')


def show_charts_menu(message, text='Какие должны быть данные'):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['charts_menu'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    titles = [f"{button_titles[title][0]} {'✅' if button_titles[title][1] else ''}" for title in button_titles.keys()]
    markup.row(titles[0], titles[1])
    markup.row(titles[2], titles[3])
    markup.add("Далее ➡️")
    markup.add("⬅️ Назад")
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.charts_menu, message.chat.id)
