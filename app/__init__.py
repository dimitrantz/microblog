from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flaskapp = Flask(__name__)
flaskapp.config.from_object(Config)
db = SQLAlchemy(flaskapp)
migrate = Migrate(flaskapp, db)

from app import routes, models
