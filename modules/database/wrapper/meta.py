from tinydb import where

from .default import TinyWrapper


class MetaWrapper(TinyWrapper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.downloads_left = self.table('downloads_left')
        self.settings = self.table('settings')

    def insert_manga_title(self, title):
        self.insert_key('manga_title', title, table=self.downloads_left.name)

    def get_manga_title(self):
        return self.get_key('manga_title', table=self.downloads_left.name, single=True)