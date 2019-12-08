from pathlib import Path

import requests
from bs4 import BeautifulSoup
from whaaaaat import prompt

from modules.error import validate
from modules.ui import Loader
from modules.ui.decorators import Loader
from .chapter import Chapter


class Manga:
    directory = Path('Manga')

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def parse(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        titlebox = soup.find(class_="manga-info-text")
        if titlebox is None:
            return self, []

        self.title = validate(titlebox.find("h1").text)

        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")

        chapter_list = []
        for i in range(len(rows) - 1, -1, -1):
            chapter_list.append(
                Chapter(validate(rows[i].find("a", href=True).text), rows[i].find("a", href=True)['href']))

        return self, chapter_list

    def path(self):
        return self.directory / Path(self.title)

    def mkdir(self, parents=True, exist_ok=True):
        self.path().mkdir(parents=parents, exist_ok=exist_ok)

    @staticmethod
    def fromdict(obj):
        if obj is None:
            return

        assert isinstance(obj, dict)

        try:
            manga = Manga(
                obj['title'],
                obj['url']
            )
            return manga
        except KeyError:
            return

    def todict(self):
        d = vars(self)
        return d

    @staticmethod
    def mkdir_base(parents=True, exist_ok=True):
        Manga.directory.mkdir(parents=parents, exist_ok=exist_ok)
