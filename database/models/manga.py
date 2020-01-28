from datetime import datetime

from network import Manga

DATETIME_FORMAT = '%Y%m%d'

class MangaModel(Manga):
    def __init__(self):
        super(MangaModel, self).__init__()

        self.manhwa = False
        self.favourite = False
        self.last_accessed = datetime.utcnow().strftime(DATETIME_FORMAT)
        self.added = datetime.utcnow().strftime(DATETIME_FORMAT)

    def persist(self, previous):
        """
        updates last_accessed and sets manhwa, favourite, and added attributes according to :param previous:
        """
        self.manhwa = previous['manhwa']
        self.favourite = previous['favourite']
        self.last_accessed = datetime.utcnow().strftime(DATETIME_FORMAT)
        self.added = previous['added']

    @staticmethod
    def from_manga(manga, **kwargs):
        """
        :param manga: manga object from network.models.Manga
        :param kwargs: these key-value pairs are mapped to the new model as attributes
        :return:
        """
        new = MangaModel()

        new.title = manga.title
        new.status = manga.status
        new.description = manga.description
        new.url = manga.url

        for key, value in kwargs.items():
            if value:
                setattr(new, key, value)

        return new

    @staticmethod
    def from_json(j):
        """
        :param j: dict
        :return: new MangaModel with corresponding dict values
        """
        new = MangaModel()

        new.title = j['title']
        new.status = j['status']
        new.description = j['description']
        new.url = j['url']
        new.manhwa = j['manhwa']
        new.favourite = j['favourite']
        new.last_accessed = datetime.strptime(j['last_accessed'], DATETIME_FORMAT)
        new.added = datetime.strptime(j['added'], DATETIME_FORMAT)

        return new