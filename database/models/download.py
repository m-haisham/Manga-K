from database import Database
from database.models import PageModel

db = Database.get()


class DownloadModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    manga = db.relationship('MangaModel', lazy=True)
    chapter = db.relationship('ChapterModel', backref=db.backref('download', uselist=False), lazy=True)

    manga_id = db.Column(db.Integer, db.ForeignKey('manga_model.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter_model.id'), nullable=False)

    def __init__(self):
        super(DownloadModel, self).__init__()

        self.value = -1
        self.max = 1

    def todict(self):
        model = vars(self).copy()
        model['pages'] = [page.to_dict() for page in self.pages]

        return model

    @staticmethod
    def fromdict(j: dict):
        model = vars(DownloadModel())

        new = DownloadModel()
        for key in model.keys():
            setattr(new, key, j[key])

        new.pages = [PageModel.from_dict(page) for page in new.pages]
        return new

    @staticmethod
    def create(manga_id, chapter_id):
        model = DownloadModel()

        model.manga_id = manga_id
        model.chapter_id = chapter_id

        return model
