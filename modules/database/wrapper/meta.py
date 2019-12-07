from .default import TinyWrapper
from ..models import Manga


class MetaWrapper(TinyWrapper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.downloads_left = self.table('downloads_left')
        self.settings = self.table('settings')

    def insert_manga(self, manga: Manga):
        self.insert_key('manga', manga.todict(), table=self.downloads_left.name)

    def get_manga(self) -> Manga:
        return Manga.fromdict(self.get_key('manga', table=self.downloads_left.name, single=True))