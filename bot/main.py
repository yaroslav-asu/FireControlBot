from bot.handlers.core import *
from bot.notifications.main import setup_notifications

setup_notifications()
bot.infinity_polling()
