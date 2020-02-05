from database import Database

db = Database.get()


class MangaMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(), nullable=False)
    manga_id = db.Column(db.Integer, db.ForeignKey('manga_model.id'), nullable=False)

    def __init__(self, key, id):
        self.key = key
        self.manga_id = id

    def __repr__(self):
        return f"MangaMap('{vars(self)}')"


class ChapterMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter_model.id'), nullable=False)

    def __init__(self, key, id):
        self.key = key
        self.chapter_id = id
