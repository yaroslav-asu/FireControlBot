from telebot import types
from bot.core.config import *
from bot.parse_data import load_fire_data
from geopy import distance

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_titles = ["Узнать о пожарах 🔥", "Посмотреть диаграммы 📊"]
    for title in button_titles:
        markup.add(title)
    bot.send_message(message.chat.id, 'Выберите то, о чем вы хотите узнать', reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.main_menu, message.chat.id)

def check_position(message):
    for i in load_fire_data([("bot/extra_data/yasen_06_2022_getFireInformationResponse.json",
                                                     "bot/extra_data/yasen_06_2022_getDynamicsResponse.json"),
                                                    ("bot/extra_data/yasen_07_2022_getFireInformationResponse.json",
                                                     "bot/extra_data/yasen_07_2022_getDynamicsResponse.json")]).values():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data['location']:
                # print(data['location'], i['coordinates']['latitude'], i['coordinates']['longitude'])
                if i['coordinates']['longitude'] and i['coordinates']['longitude']:
                    between_distance = distance.distance((i['coordinates']['longitude'], i['coordinates']['latitude']), (data['location'].longitude, data['location'].latitude)).km
                    print(between_distance, (i['coordinates']['longitude'], i['coordinates']['latitude']), (data['location'].longitude, data['location'].latitude))
@bot.message_handler(state=UserState.main_menu)
def handle_main_menu_select(message):
    from bot.interfaces.menues.charts import show_charts_menu
    from bot.interfaces.menues.fire_dates import show_fires_statistic_period_menu
    if message.text == 'Узнать о пожарах 🔥':
        check_position(message)
        show_fires_statistic_period_menu(message)
    elif message.text == 'Посмотреть диаграммы 📊':
        show_charts_menu(message)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['main_menu'] = message.text
