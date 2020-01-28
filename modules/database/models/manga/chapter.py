import requests
from bs4 import BeautifulSoup


class Chapter:
    def __init__(self, title, url, downloaded=False):

        self.title = title
        self.url = url

        assert isinstance(downloaded, bool)
        self.downloaded = downloaded

    def todict(self):
        return vars(self)

    def pages(self):
        """
        chapter_link (string): path of the chapter

        returns (list): pages of the chapter
        """
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        pagebox = soup.find(id="vungdoc")
        rows = pagebox.find_all('img')
        pages = []
        for row in rows:
            pages.append(row['src'])
        return pages

    @staticmethod
    def fromdict(obj):
        assert isinstance(obj, dict)

        try:
            chapter = Chapter(
                obj['title'],
                obj['url'],
                obj['downloaded']
            )
            return chapter
        except KeyError:
            return