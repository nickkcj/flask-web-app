from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Ana Beatriz',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'April 15, 2015'
    }
]

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html', posts=posts) #Here we are turning available the posts data to be used in the html file.

@app.route("/about")
def about_page():
    return render_template('about.html', title='About')