from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

user_favorites = db.Table('user_favorites',
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('recitals_id', db.Integer, db.ForeignKey('recitals.id'), primary_key=True)
)


class Recitals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    venue = db.Column(db.String(100), nullable=True)
    link = db.Column(db.String(200), nullable=True)
    date_string = db.Column(db.String(200), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship('Recitals', secondary=user_favorites, backref=db.backref('favorited_by', lazy='dynamic'))
