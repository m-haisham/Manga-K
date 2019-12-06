import os
import sys
import traceback
from pathlib import Path
from typing import List

from whaaaaat import prompt, Separator

from modules.MangaDownloader import MangaDownloader
from modules.codec import MKCodec
from modules.commandline import parse
from modules.composition import compose_menu
from modules.conversions import list_to_file
from modules.manager import HtmlManager, MangaManager
from modules.static import Const, visualize
from modules.styles import style
from modules.ui import colorize, Loader, Completer


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


def settings(dmanager, skip_check=False):
    if not skip_check and dmanager.settings_exists():
        # load save file
        dmanager.load_settings()

        # load settings
        settings_keys = dmanager.settings.keys()

        # print page title to console
        print('- - - Settings - - -')

        # print settings to console
        for key in settings_keys:
            print(f'[{visualize(dmanager.settings[key])}] {key.capitalize()}')

        # ask whether to change settings

        setting_change = {
            'type': 'confirm',
            'name': 'setting_change',
            'message': 'Would you like to change settings',
            'default': False
        }

        change_settings_answer = prompt(setting_change)

        make_settings = change_settings_answer['setting_change']

        # exit function, not changing settings
        if not make_settings:
            return

    # no settings saved or promted to skip, run rest of function
    else:
        if not skip_check:
            print('No Settings Saved')

    # create settings

    # whether to make composites
    make_composites = {
        'type': 'confirm',
        'name': 'make_composites',
        'message': 'Would you like to make composites',
        'default': False
    }

    composite_answer = prompt(make_composites)

    if composite_answer['make_composites']:
        make_composites = True
        # which composition type
        composition_type = {
            'type': 'list',
            'name': 'composite',
            'message': 'which format do do you want to composite to?',
            'choices': [
                'pdf',
                'image'
            ],
            'default': 0

        }

        answers = prompt(composition_type)

        composition_type = answers['composite']

        # whether to keep seperate images
        keep_originals = {
            'type': 'confirm',
            'name': 'keep_originals',
            'message': 'Would you like to keep original downloaded images?',
            'default': True
        }

        keep_original_answer = prompt(keep_originals)

        keep_originals = keep_original_answer['keep_originals']
    # default rest of settings
    elif not composite_answer['make_composites']:
        make_composites = False
        keep_originals = True
        composition_type = 'pdf'
        print('Keep_originals: True')

    dm.save_settings(make_composites, keep_originals, composition_type)


def check_files(download_manager):
    """
    Checks for existence of necessary files and folders
    """
    if not os.path.exists(Const.MangaSavePath):
        os.mkdir(Const.MangaSavePath)

    if not os.path.exists(Const.StyleSaveFile):
        list_to_file(style, Const.StyleSaveFile)
    if not download_manager.settings_exists():
        settings(download_manager)
    else:
        if not download_manager.verify_settings():
            print('Imported settings unsupported')
            settings(download_manager, skip_check=True)


if __name__ == '__main__':

    from modules import database

    database.meta_base.downloads_left = [
        dict(title='One', url='adafds'),
        dict(title='Two', url='adadffdght34erafds'),
        dict(title='Three', url='adasdasafds'),
    ]

    print(database.meta_base.downloads_left)

    database.meta_base.downloads_left = [
        dict(title='One', url='adafds'),
    ]

    print(database.meta_base.all())

    input()

    # set working directory
    os.chdir(str(Path(sys.executable if getattr(sys, 'frozen', False) else __file__).parent))

    dm: MangaDownloader = MangaDownloader()
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
            settings(dm)
        elif menuoption['menu'] == 6:
            break
        else:
            print(colorize.red('Pick a valid choice'))
