import os
from pathlib import Path

import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tinydb import Query
from tqdm import tqdm

from modules import database
from modules import resume
from modules.ImageStacking import VerticalStack, dir_to_pdf
from modules.error import decorators as error_decorators, validate
from modules.settings import get as get_settings
from modules.static import Const
from modules.ui import Loader, Completer


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

        manga_base = database.manga.databases[manga.title]
        # update manga info
        manga_base.set_manga_info(manga)
        # update manga list
        manga_base.update_chapter_list(chapters)

        # add mangas to waiting list
        resume.new(manga, to_download)

        # download each chapter loop
        for chapter in to_download:
            chapter_directory = manga_dir / Path(validate(chapter.title))

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
            # update chapters left to download, set downloaded to true
            resume.update(chapter.url)
            manga_base.chapters.update({'downloaded': True}, Query().url == chapter.url)

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
        Completer('Downloads finished').init().complete()
        print()