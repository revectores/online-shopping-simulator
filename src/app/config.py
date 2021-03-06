import os


class Config:
    DEBUG = True
    SECRET_KEY = 'ecnu'
    SQLITE3_DATABASE_PATH = os.environ.get('DB_PATH')
