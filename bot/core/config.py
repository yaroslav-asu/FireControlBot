import logging
import pathlib
import sys

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union

load_dotenv()

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class EmailSettings(BaseSettings):
    MAILGUN_API_KEY: str = "update me"
    MAILGUN_DOMAIN_NAME: str = "update me"
    MAILGUN_BASE_URL: str = "https://api.mailgun.net/v3/"
    SEND_REGISTRATION_EMAILS: bool = True


class DBSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///bot.db"
    FIRST_SUPERUSER: EmailStr = "admin@cypher.com"
    FIRST_SUPERUSER_PW: str = "CHANGEME"


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # logging levels are ints


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    email: EmailSettings = EmailSettings()
    logging: LoggingSettings = LoggingSettings()

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
