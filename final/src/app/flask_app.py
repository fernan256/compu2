import time
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash
# from mysql_connector import get_mysql_connection
from .models import db, User, Recital
from .forms import LoginForm, SignupForm, RecitalForm
from datetime import datetime


from scrappers.main import scrapper
from .config import Config
from utils import common_utils



flask_app = Flask(__name__)
flask_app.config.from_object(Config)
db.init_app(flask_app)
flask_app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@flask_app.route('/')
@login_required
def index():
    return render_template('home.html')

# def main():
#     return render_template('main.html')

@flask_app.route('/home')
@login_required
def home():
    # Check if the user is logged in
    # if 'loggedin' in session:
        # User is loggedin show them the home page
        # return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    # return redirect(url_for('login'))
    return render_template('home.html', username='diego')

@flask_app.route('/profile')
@login_required
def profile():
    # Check if the user is logged in
    # if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        # account = cursor.fetchone()
        # Show the profile page with account info
    return render_template('profile.html', account='account')
    # User is not logged in redirect to login page
    # return redirect(url_for('login'))

@flask_app.route('/recitals')
@login_required
def recitals():
    # Check if the user is logged in
    # if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        # account = cursor.fetchone()
        # Show the profile page with account info
    # scrapper('acc')
    search_results = [
        {"id": 1, "name": "diego"},
        {"id": 2, "name": "sasa 2"},
        {"id": 3, "name": "sasa 4"}
        # Add more search results as needed
    ]
    url_data = [
        {"id": 1, "url": "https://example.com", "info": "Some information about the first URL"},
        {"id": 2, "url": "https://example2.com", "info": "Information about the second URL"},
        # Add more URL data as needed
    ]
    
    return render_template('recitals.html', account='account', items=search_results, url_data=url_data)
    # User is not logged in redirect to login page
    # return redirect(url_for('login'))

@flask_app.route('/search', methods=['POST'])
@login_required
def search():
    # Retrieve the search term from the form data
    search_term = request.form.get('search')

    # Perform search logic using the search term (replace with your actual search logic)

    # Dummy search results for demonstration purposes
    search_results = [
        {"id": 1, "name": "diego"},
        {"id": 2, "name": "Result 2"},
        # Add more search results as needed
    ]

    return render_template('home.html', username="John Doe", items=search_results)


@flask_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # username = request.form['username']
        # password = request.form['password']
        # connection = get_mysql_connection()
        # # if connection:
        #     # try:
        # cursor = connection.cursor()

        # # Check if username already exists
        # cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        # user = cursor.fetchone()

        # if user:
        #     flash('Username already exists', 'warning')
        #     return render_template('register.html')

        # # Insert new user into the database
        # cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        # # cursor.commit()

        # flash('Successfully registered', 'success')
        # return redirect(url_for('index'))
        form = SignupForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            print(f"new_user: {new_user}")
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully signed up!')
            return redirect(url_for('login'))

    return render_template('register.html')

@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    http_method = request.method
    path = request.path
    protocol = request.environ.get('SERVER_PROTOCOL')
    log_message = f"Received HTTP request from {request.remote_addr}: {http_method} {path} {protocol}"
        # log_queue.put(log_message)
    common_utils.log_queue.put(log_message)
    print('hereeeeee')
    # if request.method == 'POST':
        # username = request.form['username']
        # password = request.form['password']
        # connection = get_mysql_connection()
        # # if connection:
        #     # try:
        # cursor = connection.cursor()
        # # cursor = db_connection.cursor()

        # # Check if user exists
        # cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        # user = cursor.fetchone()
        # print(f"userrrrrrrrr: {user}")
        # if not user:
        #     flash('Invalid username or password', 'danger')
        #     return render_template('login.html')

        # # Login successful
        # flash('Successfully logged in', 'success')
        # return redirect(url_for('home'))
    form = LoginForm()
    print("here1")
    if form.validate_on_submit():
        print("here1")
        identifier = form.identifier.data
        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
        if user and check_password_hash(user.password, form.password.data):
            print("here2")
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        print('not valid')
    return render_template('login.html', form=form)


url_data = [
    {"id": 1, "url": "https://example.com", "info": "Some information about the first URL"},
    {"id": 2, "url": "https://example2.com", "info": "Information about the second URL"},
    # Add more URL data as needed
]

@flask_app.route('/get_urls', methods=['GET', 'POST'])
@login_required
def get_urls():
    return render_template('get_urls.html', session={'username': 'YourUsername'}, url_data=url_data)

@flask_app.route("/update_recitals", methods=['POST'])
@login_required
def update_recitals():
    new_recitals = [
        {'artist': 'Artist 1', 'date': '2024-06-01', 'venue': 'Venue 1'},
        {'artist': 'Artist 2', 'date': '2024-07-01', 'venue': 'Venue 2'}
    ]

    for new_recital in new_recitals:
        recital_date = datetime.strptime(new_recital['date'], '%Y-%m-%d')
        existing_recital = Recital.query.filter_by(artist=new_recital['artist'], date=recital_date, venue=new_recital['venue']).first()
        if not existing_recital:
            recital = Recital(artist=new_recital['artist'], date=recital_date, venue=new_recital['venue'])
            db.session.add(recital)
    db.session.commit()
    flash('Recitals updated!', 'success')
    return redirect(url_for('recitals'))



# @flask_app.route('/')
# def index():
#     return render_template('login.html')

# @flask_app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         if username in users:
#             error = 'Username already exists'
#             return render_template('register.html', error=error)

#         # Insert new user into the placeholder data (replace with database logic)
#         users[username] = password

#         message = 'Successfully registered'
#         return redirect(url_for('index'))

#     return render_template('register.html')

# @flask_app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         if username in users and users[username] == password:
#             message = 'Successfully logged in'
#             return redirect(url_for('index'))

#         error = 'Invalid username or password'
#         return render_template('login.html', error=error)

#     return render_template('login.html')

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

