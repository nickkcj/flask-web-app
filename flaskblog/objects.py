from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a069dcf1fafbc38d6e69f8aedebd817b'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.app_context().push()
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'
    login_manager.login_message_category = 'info'


    from routes.blog_routes import routes as rt
    app.register_blueprint(rt)

    return app
