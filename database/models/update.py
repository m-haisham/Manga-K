from datetime import datetime

from database import Database

db = Database.get()


class UpdateModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    manga = db.relationship('MangaModel', backref=db.backref('updates'), lazy=True)
    chapter = db.relationship('ChapterModel', backref=db.backref('update', uselist=False), lazy=True)

    manga_id = db.Column(db.Integer, db.ForeignKey('manga_model.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter_model.id'), nullable=False)

    @staticmethod
    def create(manga_id, chapter_id):
        return UpdateModel(time=datetime.utcnow(), manga_id=manga_id, chapter_id=chapter_id)
