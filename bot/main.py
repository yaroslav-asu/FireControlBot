from telebot import custom_filters
from bot.core.logger import init_logger
from bot.handlers.core import *
from bot.notifications.main import setup_notifications


def main():
    init_logger()
    logging.info('Starting bot...')
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    logging.info('Setting up notifications...')
    setup_notifications()
    logging.info('Starting polling...')
    bot.infinity_polling()


if __name__ == '__main__':
    main()
