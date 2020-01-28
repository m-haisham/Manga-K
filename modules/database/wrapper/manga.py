from tinydb import Query

from modules.database.models import Manga, Chapter
from .default import TinyWrapper


class MangaWrapper(TinyWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.info = self.table('info')
        self.chapters = self.table('chapters')

    def get_chapter_list(self):
        docs = self.chapters.all()
        return [Chapter.fromdict(doc) for doc in docs]

    def set_info(self, manga: Manga):
        self.insert_key('info', manga.todict(), table=self.info.name)

    def get_info(self) -> Manga:
        return Manga.fromdict(self.get_key('info', table=self.info.name, single=True))

    def update_info(self, value: dict):

        manga = self.get_info()

        for key in value:
            setattr(manga, key, value[key])

        self.set_info(manga)

    def update_chapter_list(self, chapters):

        for chapter in chapters:
            # check if exists
            matches = self.chapters.search(Query().url == chapter.url)

            if len(matches) > 0:
                self.chapters.update(dict(title=chapter.title), Query().url == chapter.url)
            else:
                self.chapters.insert(chapter.todict())
