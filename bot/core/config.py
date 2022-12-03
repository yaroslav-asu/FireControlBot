import telebot
import logging
import pathlib
from dotenv import dotenv_values
from telebot.handler_backends import StatesGroup, State
from pydantic import BaseSettings, EmailStr

config = dotenv_values('.env')
bot = telebot.TeleBot(config['TOKEN'])


class UserState(StatesGroup):
    greeting = State()
    location = State()
    main_menu = State()
    fire_statistic_menu = State()
    charts_menu = State()
    select_chart_menu = State()
    chart_type = State()
    select_fires_period = State()


# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class DBSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = config['SQLALCHEMY_DATABASE_URI']
    FIRST_SUPERUSER: EmailStr = config['FIRST_SUPERUSER']
    FIRST_SUPERUSER_PW: str = config['FIRST_SUPERUSER_PW']


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # logging levels are ints


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    logging: LoggingSettings = LoggingSettings()

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
