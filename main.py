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
                    return result['href']


def direct():
    direct_question = {
        'type': 'input',
        'name': 'direct',
        'message': 'Enter the url: ',
    }

    answer = prompt(direct_question)

    return answer['direct']


def download_link(manga_url):
    # dm.print_info(manga_url)
    info = dm.get_info(manga_url)

    if not info['chapters']:
        return

    question = {
        'type': 'checkbox',
        'name': 'chapters',
        'message': 'Select chapters to download',
        'choices': [{'name': i} for i in list(info['chapters'].keys())],
    }

    answers = prompt(question)

    if not answers['chapters']:
        return

    selected_choices = [{
        'name': val,
        'href': info['chapters'][val]['href']
    } for val in answers['chapters']]

    dm.download_manga(manga_url, selected_choices)

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

    print(database.meta.get_manga_title())

    # user prompt
    print(f'Download of {len(unfinished)} {"chapter" if len(unfinished) == 1 else "chapters"} from "{database.meta.get_manga_title()}" unfinished.')
    resume = console.confirm('Would you like to resume?', default=True)

    if not resume:
        # remove all from database and exit
        database.meta.downloads_left.purge()
        return

    # start download

    dm.download_manga(
        unfinished[0]['manga_url'],
        list(map(  # change format to suit download manga
            lambda val: dict(name=val['title'], href=val['url']),
            unfinished
        ))
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
                download_link(search())
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
