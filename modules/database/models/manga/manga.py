class Manga:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(obj):
        assert isinstance(obj, dict)

        try:
            manga = Manga(
                obj['title'],
                obj['url']
            )
            return manga
        except KeyError:
            return
