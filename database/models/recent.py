from datetime import datetime

from database import Database

db = Database.get()


class RecentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.DateTime, nullable=False)
    manga = db.relationship('MangaModel', backref='recent', lazy=True)
    chapter = db.relationship('ChapterModel', backref='recent', lazy=True)

    manga_id = db.Column(db.Integer, db.ForeignKey('manga_model.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter_model.id'), nullable=False)

    DATE_FORMATTER = '%D %T'

    def __init__(self):
        super(RecentModel, self).__init__()

        self.manga_title = ''
        self.manga_link = ''
        self.accessed = datetime.now().strftime(self.DATE_FORMATTER)

    def to_dict(self):
        return vars(self)

    @staticmethod
    def create(chapter_model, title, link):
        model = RecentModel()

        copy = vars(model).copy()
        for key in copy.keys():
            try:
                setattr(model, key, getattr(chapter_model, key))
            except AttributeError:
                pass

        model.manga_title = title
        model.manga_link = link

        # pages are unnecessary
        model.pages = []

        return model
