from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
# The database can now be accessed by SQLAlchemy.
db = SQLAlchemy(app)
# Flask-Migrate is set up to work as the database migration engine.
migrate = Migrate(app, db)

# The models module will define the structure of the database.
from app import routes, models
