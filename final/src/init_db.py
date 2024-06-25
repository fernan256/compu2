from sqlalchemy import create_engine, text

from app import flask_app, db
from app.models import Users, Recitals
from app.config import Config


# Create database if it doesn't exist
def create_database_if_not_exists():
    # Create engine to connect to MySQL server (without specifying the database)
    engine = create_engine(Config.get_sqlalchemy_uri_without_db())

    # Connect to the server and create the database if it doesn't exist
    query = text(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
    with engine.connect() as connection:
        connection.execute(query)


with flask_app.app_context():
    create_database_if_not_exists()
    db.create_all()
    print("Database initialized!")
