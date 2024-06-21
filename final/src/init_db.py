from app.flask_app import flask_app, db

from app.models import Users, Recitals

with flask_app.app_context():
    db.create_all()
    print("Database initialized!")
