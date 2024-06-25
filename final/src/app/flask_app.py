import os
import time

from datetime import datetime
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect, url_for, flash
from os.path import join, dirname
from werkzeug.security import generate_password_hash

from .models import db, Users, Recitals
from .forms import LoginForm, SignupForm, RecitalForm, SearchForm
from .services import services
from .config import Config
from utils import common_utils



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

flask_app = Flask(__name__)
flask_app.config.from_object(Config)
flask_app.secret_key = os.getenv('FLASK_SECRET_KEY')

db.init_app(flask_app)

login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@flask_app.route('/')
@login_required
def index():
    common_utils.create_http_log(request)
    return render_template('home.html')


@flask_app.route('/home')
@login_required
def home():
    common_utils.create_http_log(request)
    return render_template('home.html', username='diego')


@flask_app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', account='account')


@flask_app.route("/logout")
def logout():
    common_utils.create_http_log(request)
    logout_user()
    return redirect(url_for('home'))


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    common_utils.create_http_log(request)
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


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    common_utils.create_http_log(request)
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


@flask_app.route('/search', methods=['POST'])
@login_required
def search():
    common_utils.create_http_log(request)
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.search.data
        return redirect(url_for('recitals', search_term=search_term))
    return redirect(url_for('recitals'))


@flask_app.route('/recitals')
@login_required
def recitals():
    common_utils.create_http_log(request)
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
@login_required
def add_favorite(recital_id):
    common_utils.create_http_log(request)
    services.add_favorite(current_user.id, recital_id)
    flash('Recital added to favorites.')
    return redirect(url_for('recitals'))


@flask_app.route('/remove_favorite/<int:recital_id>', methods=['POST'])
@login_required
def remove_favorite(recital_id):
    common_utils.create_http_log(request)
    services.remove_favorite(current_user.id, recital_id)
    flash('Recital removed from favorites.')
    return redirect(url_for('recitals'))


@flask_app.route('/update', methods=['POST', 'GET'])
@login_required
def update_recitals():
    common_utils.create_http_log(request)
    services.update_recitals()
    flash('Proceso de Actualizacion de recitales finalizado.')
    return redirect(url_for('recitals'))
