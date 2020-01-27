from ..models import Manga, Chapter, Page
from ..decorators import checked_connection

from typing import List


class ScraperSource:
    def get_manga_info(self, url: str) -> Manga:
        raise NotImplementedError()

    def get_chapter_list(self, manga: Manga) -> List[Chapter]:
        raise NotImplementedError()

    def get_page_list(self, chapter: Chapter) -> List[Page]:
        raise NotImplementedError()
