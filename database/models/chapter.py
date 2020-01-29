from network import Chapter


class ChapterModel(Chapter):
    def __init__(self):
        super(ChapterModel, self).__init__()

        self.downloaded = False
        self.link = ''
        self.path = ''

    def todict(self):
        return vars(self)

    @staticmethod
    def from_chapter(chapter, **kwargs):
        """
        :param kwargs: these key-value pairs are mapped to the new Chapter model as attributes
        :param chapter: chapter object from network.models.Chapter
        :return: new ChapterModel with corresponding chapter values
        """
        new = ChapterModel()

        new.title = chapter.title
        new.url = chapter.url

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

        return new