from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config.mail_config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)