from bot.utils import get_db
from bot.models.user import User
from bot.crud.crud_user import user


def start_processing(bot, message):
    # register user if not exists
    db = next(get_db())
    user_obj = db.query(User).filter(User.chat_id == int(message.chat.id)).first()
    if not user_obj:
        user_obj = user.create(db=db, data={'chat_id': int(message.chat.id)})
    db.close()

    # send greeting message
    bot.send_message(message.chat.id, "Здравствуйте, я бот для оповедения о пожарной обстановке в ХМАО, "
                                      "я буду держать вас в курсе, о статусе всех текущих пожарах, "
                                      "а так же позволю узнать сводки пожаров в этом месяце, "
                                      "году и пожароопасном сезоне"
                     )
    # send help message
