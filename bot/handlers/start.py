from bot.config import *
from bot.functions.help import show_help
from bot.interfaces.menues.main import show_main_menu
from bot.crud.crud_user import user
from bot.utils import get_db
from telebot import types
from bot.models.user import User

# greeting handler functions
@bot.message_handler(commands=['start'])
def handle_start(message):
    db = next(get_db())
    user_obj = db.query(User).filter(User.chat_id == int(message.chat.id)).first()
    if not user_obj:
        user_obj = user.create(db=db, data={'chat_id': int(message.chat.id)})
    db.close()
    bot.send_message(message.chat.id, "Здравствуйте, я бот для оповедения о пожарной обстановке в ХМАО, "
                                      "я буду держать вас в курсе, о статусе всех   текущих пожарах, "
                                      "а так же позволю узнать сводки пожаров в этом месяце, "
                                      "году и пожароопасном сезоне"
                     )
    show_help(message)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    button_skip = types.KeyboardButton(text="Пропустить")
    keyboard.add(button_geo, button_skip)
    bot.send_message(message.chat.id, "Поделитесь местоположением", reply_markup=keyboard)

@bot.message_handler(content_types=['location'])
def location (message):
    if message.location is not None:
        print(message.location)
    print(message)

    show_main_menu(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Пропустить":
        show_main_menu(message)
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю")
