import telebot
from dotenv import dotenv_values
from telebot.handler_backends import StatesGroup, State

config = dotenv_values('.env')
bot = telebot.TeleBot(config['TOKEN'])


# class Checkboxes(StatesGroup):
#     count = State()
#     causes = State()
#     area = State()
#     time = State()


class UserState(StatesGroup):
    location = State()
    main_menu = State()
    fire_statistic_menu = State()
    charts_menu = State()
    # charts_data = Checkboxes()
    select_chart_menu = State()

@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
