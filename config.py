import os
from dotenv import load_dotenv
from typing import Union

load_dotenv(verbose=True)


class Config:
    DATABSE_PORT = os.getenv("DATABASE_PORT")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = False


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True


def get_config() -> Union[ProdConfig, DevConfig]:
    if os.getenv("FLASK_ENV") == "production":
        return ProdConfig()
    else:
        return DevConfig()
