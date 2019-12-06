
class Chapter:
    def __init__(self, title, url, downloaded=False):

        self.title = title
        self.url = url

        assert isinstance(downloaded, bool)
        self.downloaded = downloaded

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)

        try:
            chapter = Chapter(
                obj['title'],
                obj['url'],
                obj['downloaded']
            )
            return chapter
        except KeyError:
            return