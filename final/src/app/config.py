import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv

current_dir = dirname(__file__)
parent_dir = abspath(join(current_dir, '..'))
dotenv_path = join(parent_dir, '.env')

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@mysql_db:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_sqlalchemy_uri():
        return Config.SQLALCHEMY_DATABASE_URI

    @staticmethod
    def get_sqlalchemy_uri_without_db():
        return f"mysql+pymysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@mysql_db:{Config.DB_PORT}/"
