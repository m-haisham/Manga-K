from whaaaaat import prompt

from modules.database import database
from modules.database.models.manga import download
from modules.ui import Loader
from modules import settings


def select_and_download(manga, chapters=None):
    if not chapters:
        with Loader("Info parse"):
            manga, chapters = manga.parse()

    exists = manga.title in database.manga.databases.keys()

    if exists:
        with Loader("Update database"):
            # check database and update get_chapter_list
            database.manga.databases[manga.title].update_chapter_list(chapters)

            # get new get_chapter_list from updated database
            chapters = database.manga.databases[manga.title].get_chapter_list()

    # get settings
    s = settings.get()

    question = {
        'type': 'checkbox',
        'name': 'get_chapter_list',
        'message': 'Select get_chapter_list to download',
        'choices': [
            dict(name=chapter.title,
                 disabled='Downloaded' if s.disable_downloaded and chapter.downloaded else False)
            for chapter in chapters],
    }

    answers = prompt(question)

    if not answers['get_chapter_list']:
        return

    selected = []
    for chapter in chapters:
        if chapter.title in answers['get_chapter_list']:
            selected.append(chapter)

    download.selective_download(manga, chapters, selected, update=not exists)
