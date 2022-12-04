from telebot import types
from bot.core.config import *
from bot.interfaces.menues.main import show_main_menu
import pyttsx3
import time
import bot.notifications.texts as texts


def show_fires_statistic_period_menu(message, buttons_state=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("За день 🚩", "За месяц 🗓️", "За год 🌲")
    markup.add("За пожароопасный сезон 🍂")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if not buttons_state:
            markup.row(f"Текст {'✅' if data['text_messages'] else ''}",
                       f"Аудио {'✅' if data['audio_messages'] else ''}")
        else:
            markup.row(f"Текст {'✅' if buttons_state[0] else ''}",
                       f"Аудио {'✅' if buttons_state[1] else ''}")
    markup.add("⬅️ Назад")
    bot.send_message(message.chat.id, 'За какой период вы хотите узнать о пожарах?', reply_markup=markup)
    bot.set_state(message.from_user.id, UserState.fire_statistic_menu, message.chat.id)


def send_audio(message, text):
    bot.send_message(message.chat.id, "Подождите, аудиосообщение уже загружается")
    tts = pyttsx3.init()

    voices = tts.getProperty('voices')
    # Задать голос по умолчанию
    tts.setProperty('voice', 'ru')

    # Попробовать установить предпочтительный голос
    for voice in voices:
        if voice.name == 'Aleksandr':
            tts.setProperty('voice', voice.id)
    tts.setProperty("rate", 150)

    tts.save_to_file(text, 'fire_information.mp3')
    tts.runAndWait()
    time.sleep(5)
    bot.send_audio(message.chat.id, open('fire_information.mp3', 'rb'))


@bot.message_handler(state=UserState.fire_statistic_menu)
def handle_fires_statistic_period(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['fire_statistic_menu'] = True
        if message.text == 'За день 🚩':
            if data['text_messages']:
                bot.send_message(message.chat.id, texts.get_summary_of_the_day())
            if data['audio_messages']:
                send_audio(message, texts.get_summary_of_the_day())
        elif message.text == 'За месяц 🗓️':
            if data['text_messages']:
                bot.send_message(message.chat.id, texts.get_summary_of_the_month())
            if data['audio_messages']:
                send_audio(message, texts.get_summary_of_the_month())
        elif message.text == 'За год 🌲':
            if data['text_messages']:
                bot.send_message(message.chat.id, texts.get_summary_of_the_year())
            if data['audio_messages']:
                send_audio(message, texts.get_summary_of_the_year())
        elif message.text == 'За пожароопасный сезон 🍂':
            if data['text_messages']:
                bot.send_message(message.chat.id, texts.get_summary_of_the_season())
            if data['audio_messages']:
                send_audio(message, texts.get_summary_of_the_season())
        elif message.text[:-2] == 'Текст' or message.text == 'Текст':
            if data['audio_messages']:
                data['text_messages'] = not data['text_messages']
                show_fires_statistic_period_menu(message, [data['text_messages'], data['audio_messages']])
            else:
                bot.send_message(message.chat.id, "Включите аудио сообщения для отключения текстовых")
        elif message.text[:-2] == 'Аудио' or message.text == 'Аудио':
            if data['text_messages']:
                data['audio_messages'] = not data['audio_messages']
                show_fires_statistic_period_menu(message, [data['text_messages'], data['audio_messages']])
            else:
                bot.send_message(message.chat.id, "Включите текстовые сообщения для отключения аудиосообщений")
        elif message.text == '⬅️ Назад':
            del data['fire_statistic_menu']
            show_main_menu(message)
