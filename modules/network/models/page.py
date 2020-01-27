
class Page:
    def __init__(self, url=None):
        if url is None:
            url = ''

        self.url = url
