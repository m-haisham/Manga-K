from datetime import datetime

from database.models import ChapterModel


class RecentModel(ChapterModel):
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
