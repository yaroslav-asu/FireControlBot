import telebot
from dotenv import dotenv_values

config = dotenv_values('.env')
bot = telebot.TeleBot(config['TOKEN'])

