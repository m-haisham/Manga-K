from tinydb import Query

from modules.database.models import Manga, Chapter
from modules.ui.decorators import Loader
from .default import TinyWrapper


class MangaWrapper(TinyWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.info = self.table('info')
        self.chapters = self.table('get_chapter_list')

    def get_chapter_list(self):
        docs = self.chapters.all()
        return [Chapter.fromdict(doc) for doc in docs]

    def set_info(self, manga: Manga):
        self.insert_key('info', manga.todict(), table=self.info.name)

    def get_info(self):
        return Manga(self.get_key('info', table=self.info.name, single=True))

    def update_chapter_list(self, chapters):

        for chapter in chapters:
            # check if exists
            matches = self.chapters.search(Query().url == chapter.url)
            # print(matches)
            if len(matches) > 0:
                self.chapters.update(dict(title=chapter.title), Query().url == chapter.url)
            else:
                self.chapters.insert(chapter.todict())