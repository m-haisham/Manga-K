from network import Page


class PageModel(Page):
    def __init__(self):
        super(PageModel, self).__init__()

        self.link = ''
        self.path = ''

    def clean_dict(self) -> dict:
        model = vars(self).copy()
        del model['path']

        return model

    def to_dict(self) -> dict:
        model = vars(self).copy()

        return model

    @staticmethod
    def from_dict(d):
        model = PageModel()

        model.url = d['url']
        model.path = d['path']
        model.link = d['link']

        return model

    @staticmethod
    def create(page, **kwargs):
        model = PageModel.from_page(page)
        model.path = kwargs['path']
        model.link = kwargs['link']

        return model

    @staticmethod
    def from_page(page):
        model = PageModel()

        model.url = page.url

        return model
