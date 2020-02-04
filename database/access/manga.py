from datetime import datetime
from typing import Union, List

import tinydb
from tinydb import Query, TinyDB

from store import slugify
from .. import mangabase


class MangaAccess:
    """
    Provides access to manga specific operations
    Only accesses manga database, its map and the specific table for the manga

    Manga title is used as key for the table
    Map is used to get the title of manga or url of chapter.
    """

    mangadb = mangabase.get()

    def __init__(self, title: str):
        self.title = title
        self.table = self.mangadb.table(title, cache_size=200)

    def set_info(self, info: dict):
        """
        Saves and overwrites information on manga

        :param info: information to be saved about this manga
        :return: None
        """
        self.mangadb.insert_key(info['url'], self.title, self.mangadb.map.name)
        self.mangadb.insert_key(slugify(info['title']), self.title, self.mangadb.map.name)
        self.mangadb.insert_key('info', info, self.title)

    def get_info(self, recorded=True) -> Union[dict, None]:
        """
        :param recorded: whether to record this access to the manga
        :return: the saved state of information
        """
        try:
            info = self.mangadb.get_key('info', self.title)
            if recorded:
                info['last_accessed'] = datetime.utcnow().strftime('%Y%m%d')
                self.set_info(info)
            return info
        except KeyError:
            pass

    def update_chapters(self, chapters):
        """
        if chapter exists Updates the chapters in database
        else adds the chapter to database and adds slog to map

        :param chapters: chapters to check against database
        :return: None
        """
        chapter_access = Query()
        for chapter in chapters:
            # check if exists
            matches = self.table.contains(chapter_access.url == chapter.url)

            if matches:
                self.table.update({
                    'title': chapter.title,
                    'link': chapter.link
                }, chapter_access.url == chapter.url)
            else:
                self.table.insert(chapter.todict())
                self.mangadb.insert_key(f'{self.title}:{slugify(chapter.title)}', chapter.url, self.mangadb.map.name)

    def update_pages(self, chapters):
        """
        Update pages of :param chapters:

        :return: None
        """
        chapter_access = Query()
        for chapter in chapters:
            self.table.update({'pages': chapter['pages']}, chapter_access.url == chapter['url'])

    def update_chapters_downloaded(self, chapters):
        """
        updates the downloaded get_status of the given chapters
        if chapter doesnt exist it is ignored

        :param chapters: chapters to update
        :return: None
        """
        chapter_access = Query()
        for chapter in chapters:
            self.table.update({'downloaded': chapter.downloaded}, chapter_access.url == chapter.url)

    def update_chapters_read(self, chapters):
        """
        updates the read status of the given chapters
        if chapter doesnt exist it is ignored

        :param chapters: chapters to update
        :return: None
        """
        chapter_access = Query()
        for chapter in chapters:
            self.table.update({'read': chapter.read}, chapter_access.url == chapter.url)

    def get_chapters(self) -> List[dict]:
        """
        :return: current stored chapters in the database
        """
        chapter_access = Query()
        return self.table.search(chapter_access.downloaded.exists())

    def get_chapter_by_slug(self, slug) -> Union[dict, None]:
        """
        :return: return chapter which has matching title to :param title:
        """
        chapter_access = Query()
        try:
            key = f'{self.title}:{slug}'
            url = self.mangadb.get_key(key, self.mangadb.map.name)

            return self.table.get(chapter_access.url == url)
        except KeyError:
            pass

    def get_chapter_by_url(self, url) -> Union[dict, None]:
        """
        :return: return chapter which has matching url to :param url:
        """
        chapter_access = Query()
        return self.table.get(chapter_access.url == url)

    def purge(self):
        """
        removes current manga table from database

        :return: None
        """
        self.mangadb.purge_table(self.title)

    @staticmethod
    def map(key):
        """
        :return: MangaAccess associated with :param key:
        """
        table = MangaAccess.mangadb.map.name

        try:
            title = MangaAccess.mangadb.get_key(key, table)
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
