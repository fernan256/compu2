import os
from os.path import join, dirname
import time
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash
from .models import db, Users, Recitals
from .forms import LoginForm, SignupForm, RecitalForm, SearchForm
from .services import services
from datetime import datetime
from .config import Config
from utils import common_utils
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
print(f"dotenv_path {dotenv_path}")
load_dotenv(dotenv_path)


flask_app = Flask(__name__)
flask_app.config.from_object(Config)
db.init_app(flask_app)
flask_app.secret_key = os.getenv('FLASK_SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@flask_app.route('/')
@login_required
def index():
    return render_template('home.html')


@flask_app.route('/home')
@login_required
def home():
    return render_template('home.html', username='diego')


@flask_app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', account='account')


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
            print(f"new_user: {new_user}")
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully signed up!')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    http_method = request.method
    path = request.path
    protocol = request.environ.get('SERVER_PROTOCOL')
    log_message = f"Received HTTP request from {request.remote_addr}: {http_method} {path} {protocol}"
    common_utils.log_queue.put(log_message)

    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data
        user = services.authenticate_user(identifier, form.password.data)
        if user:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        print('not valid')
    return render_template('login.html', form=form)


@flask_app.route('/search', methods=['POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.search.data
        return redirect(url_for('recitals', search_term=search_term))
    return redirect(url_for('recitals'))


@flask_app.route('/recitals')
@login_required
def recitals():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_term = request.args.get('search_term', '', type=str)
    if search_term:
        favorites = []
        recitals, total = services.search_recitals(search_term, page, per_page)
    else:
        recitals, favorites, total = services.get_recitals(current_user.id, page, per_page)

    return render_template('recitals.html', account='account', recitals=recitals, favorites=favorites, page=page, per_page=per_page, total=total, form=form, search_term=search_term)


@flask_app.route('/add_favorite/<int:recital_id>', methods=['POST'])
def add_favorite(recital_id):
    services.add_favorite(current_user.id, recital_id)
    flash('Recital added to favorites.')
    return redirect(url_for('recitals'))

@flask_app.route('/remove_favorite/<int:recital_id>', methods=['POST'])
def remove_favorite(recital_id):
    services.remove_favorite(current_user.id, recital_id)
    flash('Recital removed from favorites.')
    return redirect(url_for('recitals'))



@flask_app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            message = 'Successfully logged in'
            return redirect(url_for('index'))

        error = 'Invalid username or password'
        return render_template('index.html', error=error)

    return render_template('index.html')

