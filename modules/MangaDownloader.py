import json
import os
import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tinydb import Query
from tqdm import tqdm

from modules.ImageStacking import VerticalStack, dir_to_pdf
from modules.database.models import Manga
from modules.static import Const
from modules.ui import decorators, Loader

from modules import database
from modules.settings import get as get_settings
from modules.database import models

from modules.error import decorators as error_decorators


def make_valid(path):
    return re.sub('[^A-Za-z0-9 -.]+', '', path)


class MangaDownloader:
    def __init__(self):
        self.image_stacker = VerticalStack()

    def save_image(self, url, directory):
        """
        url (String): online image file path
        directory (String): Image file save path

        returns: None

        This function downloads [url] and prints the progress of the download to the console and save the file to [directory]
        """
        filename = url.split('/')[-1]
        with open(directory / Path(filename), 'wb') as f:
            response = requests.get(url, stream=True)

            total_length = response.headers.get('content-length')
            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                total_length = int(total_length)
                length_kb = round(total_length / 1024, 2)
                chunksize = int(total_length / 50)

                with tqdm(desc=f'{filename:<8}',
                          total=total_length,
                          unit='b',
                          unit_scale=True) as pbar:

                    for data in response.iter_content(chunk_size=chunksize):
                        pbar.update(len(data))
                        f.write(data)

    def get_manga_info(self, manga_path):
        """
        manga_path (string): manga path from mangakakalot.com

        return (string): manga title
        """
        r = requests.get(manga_path)
        soup = BeautifulSoup(r.content, "html.parser")
        titlebox = soup.find(class_="manga-info-text")
        title = make_valid(titlebox.find("h1").text)

        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")

        chapter_list = []
        for i in range(len(rows) - 1, -1, -1):
            chapter_list.append(models.Chapter(rows[i].find('a', href=True).text, rows[i].find('a', href=True)['href']))
            print(models.Chapter(rows[i].find('a', href=True).text, rows[i].find('a', href=True)['href']).to_dict())

        return title, chapter_list

    def get_chapter_list(self, manga_path):
        """
        manga_path (string): manga path from mangakakalot.com

        return (list): chapters of the manga
        """
        r = requests.get(manga_path)
        soup = BeautifulSoup(r.content, "html.parser")
        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")
        chapters = []
        for i in range(len(rows) - 1, -1, -1):
            chapters.append(rows[i].find('a', href=True)['href'])
        return chapters

    def get_page_list(self, chapter_path):
        """
        chapter_path (string): path of the chapter 

        returns (list): pages of the chapter
        """
        r = requests.get(chapter_path)
        soup = BeautifulSoup(r.content, "html.parser")
        pagebox = soup.find(id="vungdoc")
        rows = pagebox.find_all('img')
        pages = []
        for row in rows:
            pages.append(row['src'])
        return pages

    @error_decorators.Suppress(error_type=KeyboardInterrupt, output=True)
    def download_manga(self, manga, chapters, to_download):
        """
        url (string): manga path from mangakakalot.com
        starting_chapter (int): download start (inclusive)
        ending_chapter (int): download end (exclusive)
        chapter_list (list): optional

        returns None
        """
        # fetch settings
        settings = get_settings()

        manga_dir = Const.MangaSavePath / Path(manga.title)

        # Create directories
        Const.create_manga_save()
        manga_dir.mkdir(parents=True, exist_ok=True)
        if settings.is_compositing():
            Const.createCompositionDirs(manga_dir)

        # update base database
        database.add_manga(manga.title, manga.url, manga_dir)

        # update manga info
        database.manga.databases[manga.title].set_manga_info(manga)
        # update manga list
        database.manga.databases[manga.title].update_chapter_list(chapters)

        # delete all from downloads left
        database.meta.downloads_left.purge()

        # add manga info to download resume
        database.meta.insert_manga(manga)

        # add all new chapters to be downloaded
        database.meta.downloads_left.insert_multiple([chapter.to_dict() for chapter in to_download])

        # download each chapter loop
        for chapter in to_download:
            chapter_directory = manga_dir / Path(make_valid(chapter.title))

            # parse info
            print()
            with Loader(chapter.title):
                # create chapter dir
                chapter_directory.mkdir(parents=True, exist_ok=True)
                page_list = self.get_page_list(chapter.url)

            # download pages
            for page in page_list:
                self.save_image(page, chapter_directory)  # save image

            # on chapter download complete
            # update chapters left to download
            database.meta.downloads_left.update({'downloaded': True}, Query().url == chapter.url)
            database.manga.databases[manga.title].update({'downloaded': True}, Query().url == chapter.url)

            # convert to pdf
            if settings.pdf:
                with Loader(f'Convert {chapter_directory.parts[-1]} to pdf') as loader:
                    try:
                        dir_to_pdf(chapter_directory, os.path.join(manga_dir, Const.PdfDIr))
                    except OSError as e:
                        loader.fail(e)

            # convert to jpg
            elif settings.jpg:
                with Loader(f'Convert {chapter_directory.parts[-1]} to jpg') as loader:
                    try:
                        self.image_stacker.stack(chapter_directory, os.path.join(manga_dir, Const.JpgDir))
                    except OSError as e:
                        loader.fail(e)

        # on download task complete
