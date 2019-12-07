import os
import sys
import traceback
from pathlib import Path
from typing import List

from whaaaaat import prompt, Separator

from modules import console
from modules import database
from modules import resume
from modules import settings
from modules.codec import MKCodec
from modules.commandline import parse
from modules.composition.menu import compose_menu
from modules.console import vinput
from modules.database import models
from modules.database.models.manga.download import selective_download
from modules.manager import HtmlManager, MangaManager
from modules.static import Const
from modules.ui import colorize, Loader
from modules.console.menu import Menu
from modules import resource

def search():
    search = vinput('Enter here to search:')
    url = codec.search_prefix + search
    while True:
        codec.search(url)

        # mutate options to include page routing
        choices: List = codec.search_result[:]
        if codec.previous_page_exists():
            choices.insert(0, 'PREVIOUS')
        if codec.next_page_exists():
            choices.append('NEXT')

        search_answer = Menu('Choose', choices, key=lambda chapter: chapter['name']).prompt()

        if search_answer == 'PREVIOUS':
            url = codec.get_page(codec.current_page - 1)
            continue
        elif search_answer == 'NEXT':
            url = codec.get_page(codec.current_page + 1)
            continue
        else:
            for result in codec.search_result:
                if result['name'] == search_answer:
                    return models.Manga(result['name'], result['href'])


def direct():
    answer = vinput('Enter the url: ')

    parsed_manga, chapters = models.Manga('', answer).parse()

    return parsed_manga, chapters


def download_link(manga: models.Manga, chapters=None):
    if not chapters:
        manga, chapters = manga.parse()

    exists = manga.title in database.manga.databases.keys()

    if exists:
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
        'choices': [dict(name=chapter.title, disabled='Downloaded' if s.disable_downloaded and chapter.downloaded else False) for chapter in chapters],
    }

    answers = prompt(question)

    if not answers['get_chapter_list']:
        return

    selected = []
    for chapter in chapters:
        if chapter.title in answers['get_chapter_list']:
            selected.append(chapter)

    selective_download(manga, chapters, selected, update=not exists)


def check_files():
    """
    Checks for existence of necessary files and folders
    """
    if not os.path.exists(Const.MangaSavePath):
        os.mkdir(Const.MangaSavePath)


def continue_downloads():
    manga, unfinished = resume.get()

    if len(unfinished) <= 0:
        return

    # user prompt
    print(
        f'Download of {len(unfinished)} {"chapter" if len(unfinished) == 1 else "get_chapter_list"} from "{manga.title}" unfinished.')
    should_resume = console.confirm('Would you like to resume?', default=True)

    if not should_resume:
        # remove all from database and exit
        database.meta.downloads_left.purge()
        return

    # start download
    manga, chapters = manga.parse()
    selective_download(manga, chapters, [models.Chapter.fromdict(chapter) for chapter in unfinished], update=True)


if __name__ == '__main__':
    # set working directory
    os.chdir(str(Path(sys.executable if getattr(sys, 'frozen', False) else __file__).parent))

    resource.manager.check_resources() # mandatory resource check

    # PLAYGROUND

    # from modules.database.models import DictClass
    #
    # class ex(DictClass):
    #     def __init__(self, a, b):
    #         self.a = a,
    #         self.b = b
    #
    # input()
    # END

    continue_downloads()

    codec: MKCodec = MKCodec()
    manga_manager: MangaManager = MangaManager()
    html_manager: HtmlManager = HtmlManager()

    check_files()

    # commandline argument parse
    skip_menu, args = parse()

    while True:
        menuoption = {}
        if not skip_menu:
            mainmenu = {
                'type': 'list',
                'name': 'menu',
                'message': 'what do you wanna do?',
                'choices': [
                    'Search for manga',
                    'Open manga using direct url',
                    'View the manga',
                    Separator('-'),
                    'Compose',
                    'Settings',
                    'Exit'
                ],
                'filter': lambda val: mainmenu['choices'].index(val)
            }

            menuoption = prompt(mainmenu)
        else:
            if args.view:
                menuoption['menu'] = 2

        if menuoption['menu'] == 0:
            try:
                download_link(search())
            except Exception:
                traceback.print_exc()
        elif menuoption['menu'] == 1:
            try:
                manga, chapters = direct()
                download_link(manga, chapters)
            except Exception:
                traceback.print_exc()
        elif menuoption['menu'] == 2:
            # generate manga tree
            with Loader('Generating tree'):
                manga_manager.generate_tree()

            # generate html pages using the tree
            with Loader('Generating html files.'):
                html_manager.generate_web(manga_manager.tree)

            if html_manager.open():
                break
        elif menuoption['menu'] == 4:
            compose_menu()
        elif menuoption['menu'] == 5:
            settings.change()
        elif menuoption['menu'] == 6:
            break
        else:
            print(colorize.red('Pick a valid choice'))
