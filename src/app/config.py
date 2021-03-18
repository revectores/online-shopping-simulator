import os
from pathlib import Path


class Config:
    DEBUG = True
    SECRET_KEY = 'ecnu'
    ROOT = Path(__file__).parent
    EXPORT_PATH = ROOT / 'export'
    SQLITE3_DATABASE_PATH = ROOT / 'db/oss.db'
