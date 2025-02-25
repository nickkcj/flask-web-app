from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a069dcf1fafbc38d6e69f8aedebd817b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #Relative path from the current file

db = SQLAlchemy(app)

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

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success') #Warning, messagebox shows in screen
        return redirect(url_for('home_page'))
    return render_template('register.html', title='Register', form=form) #Same thing here, we have access to that form instance

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): #Here validates email format, etc...
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home_page'))
        
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger') #Danger here triggers a RED message instead of green.
    return render_template('login.html', title='Login', form=form)


