import os


class Config:
    DEBUG = True
    SQLITE3_DATABASE_PATH = os.environ.get('DB_PATH')

