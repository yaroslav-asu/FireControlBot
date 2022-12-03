from bot.config import *
from bot.services.help import show_help
from bot.interfaces.menues.main import show_main_menu
from bot.crud.crud_user import user
from bot.utils import get_db
from telebot import types
from bot.models.user import User


# greeting handler functions
@bot.message_handler(state="*", commands=['start'])
def handle_start(message):
    db = next(get_db())
    user_obj = db.query(User).filter(User.chat_id == int(message.chat.id)).first()
    if not user_obj:
        user_obj = user.create(db=db, data={'chat_id': int(message.chat.id)})
    db.close()
    bot.send_message(message.chat.id, "Здравствуйте, я бот для оповедения о пожарной обстановке в ХМАО - Югра, "
                                      "я буду держать вас в курсе, о статусе всех   текущих пожарах, "
                                      "а так же позволю узнать сводки пожаров в этом месяце, "
                                      "году и пожароопасном сезоне"
                     )
    show_help(message)
    bot.set_state(message.from_user.id, UserState.greeting, message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение 📍", request_location=True)
    keyboard.add(button_geo, "Пропустить ➡️")
    bot.send_message(message.chat.id, "Поделитесь местоположением", reply_markup=keyboard)


@bot.message_handler(state=UserState.greeting, content_types=['location'])
def get_location(message):
    write_location(message)


@bot.message_handler(state=UserState.greeting, content_types=['text'])
def get_skip(message):
    write_location(message)


def write_location(message):
    bot.set_state(message.from_user.id, UserState.location, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['location'] = message.location
    show_main_menu(message)
