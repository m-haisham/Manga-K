from database.models import PageModel
from database.models.chapter import ChapterModel

from store import chapter_path


class DownloadModel(ChapterModel):
    def __init__(self):
        super(DownloadModel, self).__init__()

        self.value = -1
        self.max = 1

        self.manga_title = ''
        self.manga_url = ''

        self.pages = []

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
    def create(manga, chapter, pages):
        model = DownloadModel()

        for key, value in chapter.items():
            setattr(model, key, value)

        model.path = str(chapter_path(manga['title'], chapter['title']))

        model.manga_title = manga['title']
        model.manga_url = manga['url']
        model.pages = pages

        return model