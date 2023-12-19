# IMPORT SECTION
from flask import Flask
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sahala'

from app import routes