import logging
from bot.core.config import settings


def init_logger():
    logging.basicConfig(level=settings.logging.LOGGING_LEVEL)
