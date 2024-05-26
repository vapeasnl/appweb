# Fichier : app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.views import main as main_blueprint
from app.views import auth as auth_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)

from app import models

