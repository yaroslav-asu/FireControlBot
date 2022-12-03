import schedule
from time import sleep
from threading import Thread
from functools import partial
from bot.notifications.texts import send_day_notification, send_month_notification, send_year_notification, \
    send_season_notification
from calendar import monthrange
from datetime import datetime
from datetime import date
from bot.crud.crud_user import user
from bot.core.utils import get_db

month_days_count = -1
year_days_count = -1


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def update_month_days_count():
    global month_days_count
    current_date = datetime.now()
    month_days_count = monthrange(current_date.year, current_date.month)[1]


def update_year_days_count():
    global year_days_count
    now = datetime.now()
    year_days_count = (date(now.year, 12, 31) - date(now.year, 1, 1)).days + 1


def check_season_notification(chat_id):
    if datetime.now().month == 3:
        send_season_notification(chat_id)


def setup_notifications():
    update_month_days_count()
    update_year_days_count()
    db = next(get_db())
    user_chat_ids = map(lambda x: x.chat_id, user.get_multi(db=db))

    for chat_id in user_chat_ids:
        schedule.every().day.at("12:00").do(partial(send_day_notification, chat_id))
        schedule.every(month_days_count).days.at("12:00").do(partial(send_month_notification, chat_id),
                                                             update_month_days_count)
        schedule.every(year_days_count).days.at("12:00").do(partial(send_year_notification, chat_id),
                                                            update_year_days_count)
        schedule.every().day.at("12:00").do(partial(check_season_notification, chat_id))
    Thread(target=schedule_checker).start()
