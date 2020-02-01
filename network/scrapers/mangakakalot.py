import re
from typing import List

import requests
from bs4 import BeautifulSoup

from .frame import ScraperSource
from ..decorators import checked_connection
from ..models import Chapter, Page, Manga, MangaStatus
from ..exceptions import IdentificationError, NetworkError


class Mangakakalot(ScraperSource):
    base = 'https://mangakakalot.com'

    def _encode(self, s):
        return re.sub(' ', '_', s)

    def get_manga_info(self, url: str) -> Manga:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        type = _Source.identify(url)

        instance = Manga()

        # mangakakalot.com
        if type == _Source.Mangakakalot:
            titlebox = soup.find(class_="manga-info-text")
            if titlebox is None:
                raise IdentificationError('Unable to identify title box.')

            instance.url = url
            instance.title = titlebox.find("h1").text
            instance.thumbnail_url = soup.find('div', {'class': 'manga-info-pic'}).find('img')['src']

            for box in titlebox.find_all('li'):
                if box.text.startswith('Status :'):
                    instance.status = MangaStatus.parse(box.text[9:])

                elif box.text.startswith('Genres :'):
                    instance.genres = [action.text for action in box.find_all('a', href=True)]

            _descriptionbox = soup.find('div', {'id': 'noidungm'})
            instance.description = _descriptionbox.text[len(_descriptionbox.find('h2').text):].strip()

        # manganel.com
        elif type == _Source.Manganel:
            leftpanel = soup.find(class_='story-info-right')
            if leftpanel is None:
                raise IdentificationError('Unable to identify info panel.')

            instance.url = url
            instance.title = leftpanel.find('h1').text
            instance.thumbnail_url = soup.find('span', {'class': 'info-image'}).find('img')['src']

            for box in leftpanel.find_all('tr'):
                content = box.find_all('td')
                if 'info-status' in content[0].find('i')['class']:
                    instance.status = MangaStatus.parse(content[1].text)
                elif 'info-genres' in content[0].find('i')['class']:
                    instance.genres = [action.text for action in content[1].find_all('a', href=True)]

            _descriptionbox = soup.find('div', {'id': 'panel-story-info-description'})
            instance.description = _descriptionbox.text[len(_descriptionbox.find('h3').text) + 1:].strip()

        return instance

    def get_chapter_list(self, url) -> List[Chapter]:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        type = _Source.identify(url)

        chapter_list = []
        if type == _Source.Mangakakalot:
            chapterbox = soup.find_all(class_="chapter-list")
            rows = chapterbox[0].find_all(class_="row")

            for i in range(len(rows) - 1, -1, -1):
                chapter_list.append(
                    Chapter(rows[i].find("a", href=True).text, rows[i].find("a", href=True)['href']))
        elif type == _Source.Manganel:
            rows = soup.find_all('li', {'class': 'a-h'})

            for i in range(len(rows) - 1, -1, -1):
                title = rows[i].find("a", href=True).text
                url = rows[i].find("a", href=True)['href']

                chapter_list.append(Chapter(title, url))

        return chapter_list

    def get_page_list(self, chapter: Chapter) -> List[Page]:
        r = requests.get(chapter.url)
        soup = BeautifulSoup(r.content, "html.parser")

        type = _Source.identify(chapter.url)

        if type == _Source.Mangakakalot:
            pagebox = soup.find(id="vungdoc")
        elif type == _Source.Manganel:
            pagebox = soup.find(class_="container-chapter-reader")

        rows = pagebox.find_all('img')

        pages = []
        for row in rows:
            pages.append(Page(row['src']))
        return pages

    def get_search(self, word: str, i: int) -> List[Manga]:
        url = f'{self.base}/search/{self._encode(word)}?page={i}'

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        boxes = soup.find('div', {'class': 'panel_story_list'}).find_all('div', {'class': 'story_item'})

        results = []
        for box in boxes:
            manga = Manga()

            manga.title = box.find('h3', {'class': 'story_name'}).find('a').text,
            manga.title = manga.title[0].strip(' \n')

            manga.url = box.find('a')['href']
            manga.thumbnail_url = box.find('img')['src']

            results.append(manga)

        return results

    def get_popular(self, i: int) -> List[Manga]:
        url = f'{self.base}/manga_list?type=topview&category=all&state=all&page={i}'

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        boxes = soup.find_all('div', {'class': 'list-truyen-item-wrap'})

        results = []
        for box in boxes:
            manga = Manga()

            manga.title = box.find('h3').text.strip(' \n')
            manga.url = box.find('a', href=True)['href']
            manga.thumbnail_url = box.find('img')['src']

            results.append(manga)

        return results

    def get_latest(self, i: int) -> List[Manga]:
        url = f'{self.base}/manga_list?type=latest&category=all&state=all&page={i}'

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        boxes = soup.find_all('div', {'class': 'list-truyen-item-wrap'})

        results = []
        for box in boxes:
            manga = Manga()

            manga.title = box.find('h3').text.strip(' \n')
            manga.url = box.find('a', href=True)['href']
            manga.thumbnail_url = box.find('img')['src']

            results.append(manga)

        return results


class _Source:
    Mangakakalot = 'mangakakalot'
    Manganel = 'manganel'

    @staticmethod
    def identify(url):
        """
        :param url: url to identify
        :return: source of url
        """
        if 'mangakakalot' in url:
            return _Source.Mangakakalot
        elif 'manganel' in url:
            return _Source.Manganel
        else:
            raise IdentificationError('Unable to identify source.')
