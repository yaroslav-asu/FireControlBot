from telebot import types
from bot.core.config import *
from bot.parse_data import load_fire_data
from geopy import distance


def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if check_position(message):
        markup.add("Пожар рядом с вами ⚠️")
    markup.add("Узнать о пожарах 🔥")
    markup.add("Посмотреть диаграммы 📊")
    bot.send_message(message.chat.id, 'Выберите то, о чем вы хотите узнать', reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.main_menu, message.chat.id)


def generate_caution_line():
    return ''.join(['⚠️' if i % 2 == 0 else '🔥' for i in range(12)])


def find_nearest_fire(message):
    for fire in load_fire_data([("bot/extra_data/yasen_06_2022_getFireInformationResponse.json",
                                 "bot/extra_data/yasen_06_2022_getDynamicsResponse.json"),
                                ("bot/extra_data/yasen_07_2022_getFireInformationResponse.json",
                                 "bot/extra_data/yasen_07_2022_getDynamicsResponse.json")]).values():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data['location']:
                if fire['coordinates']['longitude'] and fire['coordinates']['longitude']:
                    between_distance = distance.distance(
                        (fire['coordinates']['longitude'], fire['coordinates']['latitude']),
                        (data['location'].longitude, data['location'].latitude)).km
                    if between_distance < 5:
                        fire['distance'] = between_distance
                        return fire
    return None


@bot.message_handler(state=UserState.alert)
def see_alert_fire(message):
    if message.text == "⚠️ Узнать подробнее ➡️":
        fire = find_nearest_fire(message)
        bot.send_message(message.chat.id,
                         f"РАССТОЯНИЕ ОТ ВАС: {float('{:.2f}'.format(fire['distance'] * 1000))} метров, пожар находится в {fire['municipality']}, площадь: {fire['area']} га, возник: {fire['cause']} в {fire['date_start'].strftime('%H:%M')}, источник: {fire['cause']}")
    elif message.text == "⬅️ Назад":
        show_main_menu(message)


def show_alert_menu(message, text='Что вы хотите сделать?'):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⚠️ Узнать подробнее ➡️")
    markup.add("⬅️ Назад")
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.alert, message.chat.id)


def show_alert(message):
    bot.send_message(message.chat.id,
                     generate_caution_line() + '\nВнимание! рядом с вами обнаружен пожар!\n' + generate_caution_line(),
                     )


def check_position(message):
    for fire in load_fire_data([("bot/extra_data/yasen_06_2022_getFireInformationResponse.json",
                                 "bot/extra_data/yasen_06_2022_getDynamicsResponse.json"),
                                ("bot/extra_data/yasen_07_2022_getFireInformationResponse.json",
                                 "bot/extra_data/yasen_07_2022_getDynamicsResponse.json")]).values():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data['location']:
                # print(data['location'], i['coordinates']['latitude'], i['coordinates']['longitude'])
                if fire['coordinates']['longitude'] and fire['coordinates']['longitude']:
                    between_distance = distance.distance(
                        (fire['coordinates']['longitude'], fire['coordinates']['latitude']),
                        (data['location'].longitude, data['location'].latitude)).km
                    if between_distance < 5:
                        show_alert(message)
                        return True
    return False


@bot.message_handler(state=UserState.main_menu)
def handle_main_menu_select(message):
    from bot.interfaces.menues.charts import show_charts_menu
    from bot.interfaces.menues.fire_dates import show_fires_statistic_period_menu
    if message.text == "Пожар рядом с вами ⚠️":
        show_alert_menu(message)
    elif message.text == 'Узнать о пожарах 🔥':
        show_fires_statistic_period_menu(message)
    elif message.text == 'Посмотреть диаграммы 📊':
        show_charts_menu(message)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['main_menu'] = message.text
