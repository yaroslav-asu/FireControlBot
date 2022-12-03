from bot.config import *
from bot.functions.help import show_help


# greeting handler functions
@bot.message_handler(state="*", commands=['help'])
def handle_help(message):
    show_help(message)
