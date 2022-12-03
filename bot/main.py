from telebot import custom_filters

from bot.handlers.core import *
from bot.notifications.main import setup_notifications




bot.add_custom_filter(custom_filters.StateFilter(bot))
setup_notifications()
bot.infinity_polling()
