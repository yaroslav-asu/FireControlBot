from bot.config import *
from bot.functions.help import show_help
from bot.interfaces.menues.main import show_main_menu


# greeting handler functions
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Здравствуйте, я бот для оповедения о пожарной обстановке в ХМАО, "
                                      "я буду держать вас в курсе, о статусе всех   текущих пожарах, "
                                      "а так же позволю узнать сводки пожаров в этом месяце, "
                                      "году и пожароопасном сезоне"
                     )
    show_help(message)
    show_main_menu(message)
