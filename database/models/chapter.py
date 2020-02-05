from database import Database

db = Database.get()


class ChapterModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), unique=True, nullable=False)

    read = db.Column(db.Boolean, default=False)
    downloaded = db.Column(db.Boolean, default=False)
    path = db.Column(db.String())

    manga_id = db.Column(db.Integer, db.ForeignKey('manga_model.id'), nullable=False)

    pages = db.relationship('PageModel', backref='chapter', lazy=True)
    map = db.relationship('ChapterMap', backref='chapter', lazy=True)

    def __init__(self):
        super(ChapterModel, self).__init__()

        self.downloaded = False
        self.read = False
        self.link = ''
        self.path = ''
        self.pages = []

    def todict(self):
        return vars(self)

    @staticmethod
    def from_chapter(chapter, manga_id, **kwargs):
        """
        :param kwargs: these key-value pairs are mapped to the new Chapter model as attributes
        :param chapter: chapter object from network.models.Chapter
        :return: new ChapterModel with corresponding chapter values
        """
        new = ChapterModel()

        new.title = chapter.title
        new.url = chapter.url
        new.manga_id = manga_id

        for key, value in kwargs.items():
            if value:
                setattr(new, key, value)

        return new

    @staticmethod
    def fromdict(j: dict):
        """
        :param j: dict
        :return: new ChapterModel with corresponding dict values
        """
        new = ChapterModel()

        new.title = j['title']
        new.url = j['url']
        new.downloaded = j['downloaded']
        new.link = j['link']
        new.path = j['path']
        new.pages = j['pages']

        return new

    def __repr__(self):
        return f"Chapter('{self.title}', '{self.url}')"
