from .default import TinyWrapper

class MangaWrapper(TinyWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.info = self.table('info')
        self.chapters = self.table('chapters')