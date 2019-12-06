import requests
from bs4 import BeautifulSoup

from modules.error import validate
from modules.ui.decorators import Loader
from .chapter import Chapter
from .manga import Manga


@Loader(message='Parse info')
def parse(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    titlebox = soup.find(class_="manga-info-text")
    title = titlebox.find("h1").text

    chapterbox = soup.find_all(class_="chapter-list")
    rows = chapterbox[0].find_all(class_="row")

    chapter_list = []
    for i in range(len(rows) - 1, -1, -1):
        chapter_list.append(Chapter(rows[i].find("a", href=True).text, rows[i].find("a", href=True)['href']))

    return Manga(validate(title), url), chapter_list
