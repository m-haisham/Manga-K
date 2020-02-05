from datetime import datetime

from network import Manga
from store import manga_path
from ..database import Database
from ..types import ArrayType, PathType

DATETIME_FORMAT = '%D %T'

db = Database.get()


class MangaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String())
    genres = db.Column(ArrayType())
    url = db.Column(db.String(), unique=True, nullable=False)
    path = db.Column(PathType())

    thumbnail_url = db.Column(db.String())

    manhwa = db.Column(db.Boolean, default=False)
    favourite = db.Column(db.Boolean, default=False)
    added = db.Column(db.DateTime, default=datetime.utcnow)

    chapters = db.relationship('ChapterModel', backref='manga', lazy=True)
    map = db.relationship('MangaMap', backref='manga', lazy=True)

    def persist(self, previous):
        """
        updates last_accessed and sets manhwa, favourite, and added attributes according to :param previous:
        """
        self.manhwa = previous['manhwa']
        self.favourite = previous['favourite']
        self.added = previous['added']

    def to_dict(self):
        return vars(self).copy()

    @staticmethod
    def from_manga(manga, **kwargs):
        """
        :param manga: manga object from network.models.Manga
        :param kwargs: these key-value pairs are mapped to the new model as attributes
        :return:
        """
        new = MangaModel()

        for key in vars(Manga()).keys():
            setattr(new, key, getattr(manga, key))

        for key, value in kwargs.items():
            if value is not None:
                setattr(new, key, value)

        new.path = manga_path(manga.title)

        return new

    @staticmethod
    def from_json(j):
        """
        :param j: dict
        :return: new MangaModel with corresponding dict values
        """
        new = MangaModel()

        for key in vars(new).keys():
            setattr(new, key, j[key])

        return new

    def __repr__(self):
        return f"Manga('{self.title}', '{self.url}')"
