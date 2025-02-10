from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home_page():
    return "<h1>Home Page</h1>"

@app.route("/about")
def about_page():
    return "<h1>About Page</h1>"