import requests
from bs4 import BeautifulSoup

from .manga import Manga
from .chapter import Chapter

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

    return Manga(title, url), chapter_list