import os
import sys
import traceback
from pathlib import Path
from typing import List

from tinydb import where
from whaaaaat import prompt, Separator

from modules.MangaDownloader import MangaDownloader
from modules.codec import MKCodec
from modules.commandline import parse
from modules.composition import compose_menu
from modules.conversions import list_to_file
from modules.manager import HtmlManager, MangaManager
from modules.static import Const
from modules.console.display import visualize
from modules.styles import style
from modules.ui import colorize, Loader, Completer
from modules import console

from modules import database
from modules import settings
from modules.database import models
from modules.database.models.manga import parse as manga_parse

def search():
    search_question = {
        'type': 'input',
        'name': 'search',
        'message': 'Enter here to search: '
    }

    search_answer = prompt(search_question)

    search = search_answer['search']
    url = codec.search_prefix + search
    while True:
        codec.search(url)

        # mutate options to include page routing
        choices: List = codec.search_result[:]
        if codec.previous_page_exists():
            choices.insert(0, 'PREVIOUS')
        if codec.next_page_exists():
            choices.append('NEXT')

        search_question = {
            'type': 'list',
            'name': 'search',
            'message': 'choose',
            'choices': choices
        }

        search_answer = prompt(search_question)

        if search_answer['search'] == 'PREVIOUS':
            url = codec.get_page(codec.current_page - 1)
            continue
        elif search_answer['search'] == 'NEXT':
            url = codec.get_page(codec.current_page + 1)
            continue
        else:
            for result in codec.search_result:
                if result['name'] == search_answer['search']:
                    return result['name'], result['href']


def direct():
    direct_question = {
        'type': 'input',
        'name': 'direct',
        'message': 'Enter the url: ',
    }

    answer = prompt(direct_question)['direct']

    return manga_parse(answer)


def download_link(title, url):
    # dm.print_info(manga_url)
    manga, chapters = manga_parse(url)

    if not chapters:
        return

    question = {
        'type': 'checkbox',
        'name': 'chapters',
        'message': 'Select chapters to download',
        'choices': [{'name': i.title} for i in chapters],
    }

    answers = prompt(question)

    if not answers['chapters']:
        return

    selected = []
    for chapter in chapters:
        if chapter.title in answers['chapters']:
            selected.append(chapter)

    dm.download_manga(models.Manga(title, url), chapters, selected)

def check_files(download_manager):
    """
    Checks for existence of necessary files and folders
    """
    if not os.path.exists(Const.MangaSavePath):
        os.mkdir(Const.MangaSavePath)

    if not os.path.exists(Const.StyleSaveFile):
        list_to_file(style, Const.StyleSaveFile)


def continue_downloads():
    unfinished = database.meta.downloads_left.search(where('downloaded') == False)

    if len(unfinished) <= 0:
        return

    manga = database.meta.get_manga()

    # user prompt
    print(f'Download of {len(unfinished)} {"chapter" if len(unfinished) == 1 else "chapters"} from "{manga.title}" unfinished.')
    resume = console.confirm('Would you like to resume?', default=True)

    if not resume:
        # remove all from database and exit
        database.meta.downloads_left.purge()
        return

    # start download
    manga, chapters = manga_parse(manga.url)
    dm.download_manga(
        manga,
        chapters,
        [models.Chapter.from_dict(chapter) for chapter in unfinished]
    )


dm: MangaDownloader = MangaDownloader()

if __name__ == '__main__':
    # set working directory
    os.chdir(str(Path(sys.executable if getattr(sys, 'frozen', False) else __file__).parent))

    # PLAYGROUND

    # from modules import settings
    #
    # settings.change()
    #
    # input()
    # END

    continue_downloads()

    codec: MKCodec = MKCodec()
    manga_manager: MangaManager = MangaManager()
    html_manager: HtmlManager = HtmlManager()

    check_files(dm)

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
                'filter': lambda val: mainmenu['choices'].index(val),
                'default': 4

            }

            menuoption = prompt(mainmenu)
        else:
            if args.view:
                menuoption['menu'] = 2

        if menuoption['menu'] == 0:
            try:
                title, chapters = search()
                download_link(title, chapters)
            except Exception:
                traceback.print_exc()
        elif menuoption['menu'] == 1:
            try:
                download_link(direct())
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
