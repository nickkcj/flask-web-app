import secrets, os
from flask import render_template, url_for, flash, redirect, Blueprint, request, current_app
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

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
    if current_user.is_authenticated:
        return redirect(url_for('routes.home_page'))
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
    if current_user.is_authenticated:
        return redirect(url_for('routes.home_page'))
    form = LoginForm()
    if form.validate_on_submit(): #Here validates email format, etc...
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #Here we check if the user exists and if the password is correct
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else (url_for('routes.home_page')) #If everything is correct, we redirect to the home page
        
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger') #Danger here triggers a RED message instead of green.
    return render_template('login.html', title='Login', form=form)

@routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('routes.home_page'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@routes.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('routes.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form) 