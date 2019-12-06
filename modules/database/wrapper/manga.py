from tinydb import Query

from modules.database.models import Manga
from .default import TinyWrapper
from modules.ui.decorators import Loader

class MangaWrapper(TinyWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.info = self.table('info')
        self.chapters = self.table('chapters')

    def set_manga_info(self, manga: Manga):
        self.insert_key('info', manga.to_dict(), table=self.info.name)

    def get_manga_info(self):
        return self.get_key('info', table=self.info.name, single=True)

    @Loader(message='Update database')
    def update_chapter_list(self, chapters):

        for chapter in chapters:
            # check if exists
            matches = self.chapters.search(Query().url == chapter.url)
            # print(matches)
            if len(matches) > 0:
                self.chapters.update(dict(title=chapter.title), Query().url == chapter.url)
            else:
                self.chapters.insert(chapter.to_dict())
