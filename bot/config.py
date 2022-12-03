import telebot
from dotenv import dotenv_values
from telebot.handler_backends import StatesGroup, State

config = dotenv_values('.env')
bot = telebot.TeleBot(config['TOKEN'])


class UserState(StatesGroup):
    greeting = State()
    location = State()
    main_menu = State()
    fire_statistic_menu = State()
    charts_menu = State()
    select_chart_menu = State()
    chart_type = State()
    select_fires_period = State()
