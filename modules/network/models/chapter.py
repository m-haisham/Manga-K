
class Chapter:
    def __init__(self, title=None, url=None):
        if title is None:
            title = ''

        self.title = title

        if url is None:
            url = ''

        self.url = url
