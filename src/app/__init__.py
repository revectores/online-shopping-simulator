from flask import Flask
app = Flask(__name__)

from app import route
from app.config import Config

app.config.from_object(Config)
