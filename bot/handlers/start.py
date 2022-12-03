from bot.config import *
from bot.functions.help import show_help
from bot.interfaces.menues.main import show_main_menu
from bot.crud.crud_user import user
from bot.utils import get_db
from telebot import types


# greeting handler functions
@bot.message_handler(commands=['start'])
def handle_start(message):
    db = next(get_db())
    usera = user.create(db=db, data={'chat_id': int(message.chat.id)})
    _ = user.update(db=db, db_obj=usera, data={'chat_id': 123})
    db.close()
    bot.send_message(message.chat.id, "Здравствуйте, я бот для оповедения о пожарной обстановке в ХМАО, "
                                      "я буду держать вас в курсе, о статусе всех   текущих пожарах, "
                                      "а так же позволю узнать сводки пожаров в этом месяце, "
                                      "году и пожароопасном сезоне"
                     )
    show_help(message)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Поделитесь местоположением", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    if message.location is not None:
        print(message.location)
    print(message)

    show_main_menu(message)
