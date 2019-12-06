from tinydb import where

from .default import TinyWrapper


class MetaWrapper(TinyWrapper):
    dleft = 'chapter_downloads_left'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def downloads_left(self):
        docs = self.search(where('type') == self.dleft)
        if len(docs) == 1:
            return docs[0]
        else:
            return docs

    @downloads_left.setter
    def downloads_left(self, value):
        self.upsert(dict(type=self.dleft, data=value), where('type') == self.dleft)

    @downloads_left.deleter
    def downloads_left(self):
        self.upsert(dict(type=self.dleft, data=[]), where('type') == self.dleft)