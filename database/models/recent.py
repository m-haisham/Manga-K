from datetime import datetime

from database import Database

db = Database.get()


class RecentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.DateTime, nullable=False)
    manga = db.relationship('MangaModel', backref=db.backref('recent', uselist=False), lazy=True)
    chapter = db.relationship('ChapterModel', backref=db.backref('recent', uselist=False), lazy=True)

    manga_id = db.Column(db.Integer, db.ForeignKey('manga_model.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter_model.id'), nullable=False)

    DATE_FORMATTER = '%D %T'

    @staticmethod
    def create(manga_id, chapter_id):
        return RecentModel(time=datetime.utcnow(), manga_id=manga_id, chapter_id=chapter_id)
