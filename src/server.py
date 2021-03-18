from app import app
from app.model import db_init
from app.config import Config
from pathlib import Path

if __name__ == '__main__':
	import os
	if not os.path.exists(Config.ROOT / 'db' / 'oss.db'):
		db_init()

	if not os.path.exists(Config.EXPORT_PATH):
		os.mkdir(Config.EXPORT_PATH)

	app.run()
