from flask_app import flask_app, db

from models import User, Recital

with flask_app.app_context():
    db.create_all()
    print("Database initialized!")
