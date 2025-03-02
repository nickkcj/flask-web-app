from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.routes import routes as rt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a069dcf1fafbc38d6e69f8aedebd817b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #Relative path from the current file
db = SQLAlchemy(app)
app.register_blueprint(rt)