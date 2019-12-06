from tinydb import where

from .default import TinyWrapper


class MetaWrapper(TinyWrapper):
    dleft = 'chapter_downloads_left'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def downloads_left(self):
        return self.all()[self.dleft]

    @downloads_left.setter
    def downloads_left(self, value):
        self.upsert(value, where(self.dleft))