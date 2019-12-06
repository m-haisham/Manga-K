from tinydb import where

from ..models import Manga
from .default import TinyWrapper


class MetaWrapper(TinyWrapper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.downloads_left = self.table('downloads_left')
        self.settings = self.table('settings')

    def insert_manga(self, manga: Manga):
        self.insert_key('manga', manga.to_dict(), table=self.downloads_left.name)

    def get_manga(self) -> Manga:
        return Manga.from_dict(self.get_key('manga', table=self.downloads_left.name, single=True))