from pathlib import Path

import requests
from bs4 import BeautifulSoup

from modules.ui.decorators import Loader
from .chapter import Chapter


class Manga:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.directory = Path('Manga')

    @Loader(message='Parse info')
    def parse(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        titlebox = soup.find(class_="manga-info-text")
        self.title = titlebox.find("h1").text

        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")

        chapter_list = []
        for i in range(len(rows) - 1, -1, -1):
            chapter_list.append(Chapter(rows[i].find("a", href=True).text, rows[i].find("a", href=True)['href']))

        return self, chapter_list

    def todict(self):
        d = vars(self)
        d['directory'] = str(d['directory'])

        return d

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
