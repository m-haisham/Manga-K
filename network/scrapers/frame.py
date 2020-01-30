from ..models import Manga, Chapter, Page
from ..decorators import checked_connection

from typing import List


class ScraperSource:
    def get_manga_info(self, url: str) -> Manga:
        """
        downloads the website and extracts key information

        :information: title, get_status, and description

        :param url: url of manga
        :return: manga object
        """
        raise NotImplementedError()

    def get_chapter_list(self, url) -> List[Chapter]:
        """
        downloads website and extracts chapters

        :param url: url to which chapters belong to
        :return: list of chapter objects
        """
        raise NotImplementedError()

    def get_page_list(self, chapter: Chapter) -> List[Page]:
        """
        downloads webpage and extracts pages

        :param chapter: chapter [url] to which pages belong to
        :return: list of page objects
        """
        raise NotImplementedError()

    def get_search(self, word: str, i: int) -> List[Manga]:
        """
        downloads webpage and extracts contents to list

        :param word: word to use for search
        :param i: index of page of search
        :return: list of mangas
        """
        raise NotImplementedError()

    def get_popular(self, i: int) -> List[Manga]:
        """
        downloads webpage and extracts contents to list

        :param i: index of page of page
        :return: list of mangas
        """
        raise NotImplementedError()

    def get_latest(self, i: int) -> List[Manga]:
        """
        downloads webpage and extracts contents to list

        :param i: index of page of page
        :return: list of mangas
        """
        raise NotImplementedError()

