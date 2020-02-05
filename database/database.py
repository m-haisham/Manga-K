from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker


class Database:
    _instance = None

    def __init__(self, app):
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
        self.db = SQLAlchemy(app)

    @staticmethod
    def get() -> SQLAlchemy:
        return Database._instance.db


class LocalSession:
    Factory = None
    session = None

    def __enter__(self):
        return self.Factory()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Factory.remove()


def set(app):
    Database._instance = Database(app)
    LocalSession.session = Database.get().session
    LocalSession.Factory = scoped_session(sessionmaker(bind=Database.get().engine))
