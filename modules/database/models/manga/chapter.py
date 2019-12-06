
class Chapter:
    def __init__(self, title, url, manga_url, downloaded=False):

        self.title = title
        self.manga_url = manga_url
        self.url = url

        assert isinstance(downloaded, bool)
        self.downloaded = downloaded

    def to_dict(self):
        return vars(self)