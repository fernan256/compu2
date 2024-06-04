from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import Config
from contextlib import contextmanager

# Create an engine
engine = create_engine(Config.get_sqlalchemy_uri(), pool_pre_ping=True)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
