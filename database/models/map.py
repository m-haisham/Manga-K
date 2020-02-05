from database import Database

db = Database.get()


class MangaMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(), nullable=False)
    manga_id = db.Column(db.Integer, db.ForeignKey('mangamodel.id'), nullable=False)


class ChapterMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chaptermodel.id'), nullable=False)
