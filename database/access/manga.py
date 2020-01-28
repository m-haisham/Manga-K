from datetime import datetime

import tinydb
from tinydb import Query, TinyDB

from .. import mangabase


class MangaAccess:
    mangadb = mangabase.get()

    def __init__(self, title: str):
        self.title = title
        self.table = self.mangadb.table(title)

    def set_info(self, info: dict):
        """
        Saves and overwrites information on manga

        :param info: information to be saved about this manga
        :return: None
        """
        self.mangadb.insert_key(info['url'], self.title, self.mangadb.map.name)
        self.mangadb.insert_key('info', info, self.title)

    def get_info(self, recorded=True) -> dict:
        """
        :param recorded: whether to record this access to the manga
        :return: the saved state of information
        """
        try:
            info = self.mangadb.get_key('info', self.title, single=True)
            if recorded:
                info['last_accessed'] = datetime.utcnow().strftime('%Y%m%d')
                self.set_info(info)
            return info
        except KeyError:
            pass

    def update_chapters(self, chapters):
        """
        if chapter exists Updates the chapters in database
        else adds the chapter to database

        :param chapters: chapters to check against database
        :return: None
        """
        chapter_access = Query()
        for chapter in chapters:
            # check if exists
            matches = self.table.contains(chapter_access.url == chapter.url)

            if matches:
                self.table.update(dict(title=chapter.title, link=chapter.link), chapter_access.url == chapter.url)
            else:
                self.table.insert(chapter.todict())

    def get_chapters(self):
        """
        :return: current stored chapters in the database
        """
        chapter_access = Query()
        return self.table.search(chapter_access.downloaded.exists())

    def get_chapter(self, title):
        """
        :return: return chapter which has matching title to :param title:
        """
        chapter_access = Query()
        try:
            return self.table.search(chapter_access.title == title)[0]
        except IndexError:
            return None

    def purge(self):
        """
        removes current manga table from database

        :return: None
        """
        self.mangadb.purge_table(self.title)

    @staticmethod
    def url(url):
        """
        :return: MangaAccess associated with :param url:
        """
        try:
            title = MangaAccess.mangadb.get_key(url, MangaAccess.mangadb.map.name, single=True)
            return MangaAccess(title)
        except KeyError:
            pass

    @staticmethod
    def all():
        """
        :return: name of all manga tables in database
        """
        return [table for table in MangaAccess.mangadb.tables() if
                table not in [TinyDB.DEFAULT_TABLE, MangaAccess.mangadb.map.name]]
