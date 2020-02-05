from pathlib import Path

from database import Database
from database.types import PathType

db = Database.get()


class Thumbnail(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String(), unique=True, nullable=False)
    path = db.Column(PathType(), nullable=False)
    manga = db.relationship('MangaModel', backref='thumbnail', lazy=True)

    manga_id = db.Column(db.Integer, db.ForeignKey('manga_model.id'), nullable=False)

    def __init__(self, title, url, manga_id):
        self.path = self.thumbnail_path(title)
        self.url = url
        self.manga_id = manga_id

    @staticmethod
    def thumbnail_path(manga_path):
        return manga_path / Path('thumbnail.jpg')