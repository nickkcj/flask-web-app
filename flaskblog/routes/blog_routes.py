from flask import render_template, url_for, flash, redirect, Blueprint
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
routes = Blueprint("routes", __name__)

from flaskblog.objects import db, bcrypt

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

@routes.route("/")
@routes.route("/home")
def home_page():
    return render_template('home.html', posts=posts) #Here we are turning available the posts data to be used in the html file.

@routes.route("/about")
def about_page():
    return render_template('about.html', title='About')

@routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success') #Warning, messagebox shows in screen
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form) #Same thing here, we have access to that form instance

@routes.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): #Here validates email format, etc...
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('.home_page'))
        
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger') #Danger here triggers a RED message instead of green.
    return render_template('login.html', title='Login', form=form)