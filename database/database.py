import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TypeDecorator, String
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
    session = None

    def __enter__(self):
        self.session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.remove()


def set(app):
    Database._instance = Database(app)
    LocalSession.session = scoped_session(sessionmaker(bind=Database.get().engine))


class ArrayType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return ArrayType(self.impl.length)
