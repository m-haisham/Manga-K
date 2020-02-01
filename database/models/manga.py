from datetime import datetime

from network import Manga

DATETIME_FORMAT = '%D %T'


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

        for key in vars(new).keys():
            setattr(new, key, j[key])

        return new
