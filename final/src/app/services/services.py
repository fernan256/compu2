from datetime import datetime
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

from app.models import Users, Recitals
from app.config import Config
from scrapers import save_recitals


engine = create_engine(Config.get_sqlalchemy_uri(), pool_pre_ping=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


def create_user(username, password, email):
    with get_db_session() as session:
        existing_user = session.query(Users).filter_by(username=username).first()
        if existing_user:
            raise ValueError("Username already exists")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = Users(username=username, password=hashed_password, email=email)
        session.add(new_user)
        session.commit()


def authenticate_user(username, password):
    with get_db_session() as session:
        user = session.query(Users).filter((Users.username == username) | (Users.email == username)).first()
        if user and check_password_hash(user.password, password):
            return user
        return None


def get_recitals(user_id, page=1, per_page=10):
    with get_db_session() as session:
        total = session.query(Recitals).filter(Recitals.is_deleted == 0).count()
        recitals = session.query(Recitals).filter(Recitals.is_deleted == 0).offset((page - 1) * per_page).limit(per_page).all()
        
        user = session.query(Users).get(user_id)
        favorites = user.favorites if user else []
        
        return recitals, favorites, total

    
def search_recitals(search_term, page=1, per_page=10):
    with get_db_session() as session:
        query = session.query(Recitals).filter(
            or_(
                Recitals.artist.ilike(f'%{search_term}%'),
                Recitals.venue.ilike(f'%{search_term}%')
            )
        )
        total = query.count()
        recitals = query.offset((page - 1) * per_page).limit(per_page).all()
        return recitals, total


def remove_old_events():
    with get_db_session() as session:
        current_date = datetime.now()
        past_recitals = session.query(Recitals).filter(
                    Recitals.date < current_date,
                    Recitals.is_deleted == False
                ).all()
        for recital in past_recitals:
                recital.is_deleted = True
        session.commit()
        

def add_recital(artist, date, date_string, venue, link):
    with get_db_session() as session:
        new_recital = Recitals(artist=artist, date=date, date_string=date_string, venue=venue, link=link)
        session.add(new_recital)
        session.commit()


def add_favorite(user_id, recital_id):
    with get_db_session() as session:
        user = session.query(Users).get(user_id)
        recital = session.query(Recitals).get(recital_id)
        if recital not in user.favorites:
            user.favorites.append(recital)
            session.commit()
        return True


def remove_favorite(user_id, recital_id):
    with get_db_session() as session:
        user = session.query(Users).get(user_id)
        recital = session.query(Recitals).get(recital_id)
        if recital in user.favorites:
            user.favorites.remove(recital)
            session.commit()
        return True


def update_recitals():
    manager = save_recitals.ScraperManager()
    manager.run()