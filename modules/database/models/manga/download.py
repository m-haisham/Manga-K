from pathlib import Path

import requests
from pynotifier import Notification
from tinydb import Query
from tqdm import tqdm
from whaaaaat import prompt

import modules.database.mangas
from modules import composition
from modules import resume
from modules.composition import dir_to_jpg, dir_to_pdf
from modules.database.mangas import manga as saved_manga
from modules.error import decorators as error
from modules.settings import get as get_settings
from modules.ui import Loader, Completer
from .manga import Manga


def save_image(url, directory):
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
            chunksize = int(total_length / 50)

            with tqdm(desc=f'{filename:<8}',
                      total=total_length,
                      unit='b',
                      unit_scale=True) as pbar:

                for data in response.iter_content(chunk_size=chunksize):
                    pbar.update(len(data))
                    f.write(data)


@error.Suppress(error_type=KeyboardInterrupt, output=True)
def selective_download(manga, chapters, to_download, update=False):
    """
    url (string): manga path from mangakakalot.com
    starting_chapter (int): download start (inclusive)
    ending_chapter (int): download end (exclusive)
    chapter_list (list): optional

    returns None
    """
    # fetch settings
    settings = get_settings()

    manga_path = manga.path()

    # Create directories
    Manga.mkdir_base()
    if settings.is_compositing():
        composition.dir.create_directories(manga)

    # update base database
    modules.database.mangas.add_manga(manga.title, manga.url, manga_path)

    manga_base = modules.database.mangas.manga.databases[manga.title]
    # update manga info
    manga_base.set_info(manga)

    if update:
        with Loader("Update database"):
            # update chapter list
            manga_base.update_chapter_list(chapters)

    # add mangas to waiting list
    resume.new(manga, to_download)

    # download each chapter loop
    for chapter in to_download:
        chapter_directory = manga_path / Path(chapter.title)

        # parse info
        print()
        with Loader(chapter.title):
            # create chapter dir
            chapter_directory.mkdir(parents=True, exist_ok=True)
            page_list = chapter.pages()

        # download pages
        for page in page_list:
            save_image(page, chapter_directory)  # save image

        # on chapter download complete
        # update chapters left to download, set downloaded to true
        resume.update(chapter.url)
        manga_base.chapters.update({'downloaded': True}, Query().url == chapter.url)

        # convert to pdf
        if settings.pdf:
            with Loader(f'Convert {chapter_directory.parts[-1]} to pdf') as loader:
                try:
                    dir_to_pdf(chapter_directory, manga_path / composition.directories.pdf)
                except OSError as e:
                    loader.fail(e)

        # convert to jpg
        if settings.jpg:
            with Loader(f'Convert {chapter_directory.parts[-1]} to jpg') as loader:
                try:
                    dir_to_jpg(chapter_directory, manga_path / composition.directories.jpg)
                except OSError as e:
                    loader.fail(e)

    # on download task complete
    Completer('Downloads complete').init().complete()

    # download task complete notification
    Notification(
        title='Download task complete',
        description=f'{manga.title} | {len(to_download)} chapters downloaded'
    ).send()

    print()


def select_and_download(manga, chapters=None):
    if not chapters:
        with Loader("Parse Info"):
            manga, chapters = manga.parse()

    exists = manga.title in saved_manga.databases.keys()

    if exists:
        with Loader("Update database"):
            # check database and update chapters
            saved_manga.databases[manga.title].update_chapter_list(chapters)

            # get new chapters from updated database
            chapters = saved_manga.databases[manga.title].get_chapter_list()

    # get settings
    s = get_settings()

    question = {
        'type': 'checkbox',
        'name': 'chapters',
        'message': 'Select chapters to download',
        'choices': [
            dict(name=chapter.title,
                 disabled='Downloaded' if s.disable_downloaded and chapter.downloaded else False)
            for chapter in chapters],
    }

    answers = prompt(question)

    if not answers['chapters']:
        return

    selected = []
    for chapter in chapters:
        if chapter.title in answers['chapters']:
            selected.append(chapter)

    selective_download(manga, chapters, selected, update=not exists)
