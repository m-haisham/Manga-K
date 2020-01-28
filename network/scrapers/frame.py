from ..models import Manga, Chapter, Page
from ..decorators import checked_connection

from typing import List


class ScraperSource:
    def get_manga_info(self, url: str) -> Manga:
        """
        downloads the website and extracts key information

        :information: title, status, and description

        :param url: url of manga
        :return: manga object
        """
        raise NotImplementedError()

    def get_chapter_list(self, manga: Manga) -> List[Chapter]:
        """
        downloads website and extracts chapters

        :param manga: manga [url] to which chapters belong to
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

    # TODO search by keywords
    # TODO popular
    # TODO latest
