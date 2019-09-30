import os
import traceback

from whaaaaat import prompt, Separator

from modules.codec import MKCodec
from modules.conversions import create_py_list, list_to_file
from modules.manager import HtmlManager, MangaManager
from modules.MangaDownloader import MangaDownloader
from modules.static import Const
from modules.styles import style


def search():

    search_question = {
        'type': 'input',
        'name': 'search',
        'message': 'Enter here to search: '
    }

    search_answer = prompt(search_question)

    search = search_answer['search']
    url = codec.search_prefix+search
    complete = False
    while not complete:
        codec.search(url)

        for i in range(len(codec.search_result)):
            result = codec.search_result[i]
            print(str(i + 1), end=") ")
            print(result['name'])

        # if only one page is in result
        if codec.max_page == -1:
            pass
        else:
            print('page '+str(codec.current_page)+' of '+str(codec.max_page))

        while True:
            print('To Pick a page put p followed by page number.')
            input_key = input('Pick number corresponding to choice: ')

            try:
                index = int(input_key) - 1
            except ValueError:
                if input_key[0].lower() == 'p':
                    try:
                        page = int(input_key[1:])
                    except ValueError:
                        print("Invalid Input\n")
                        continue
                    if page < 1 or page > codec.max_page:
                        print("Invalid Page Number\n")
                        continue
                    if codec.search_prefix+search+codec.search_postfix+str(page) == url:
                        print('Same Page Selected')
                        continue
                    else:
                        url = codec.search_prefix+search + \
                            codec.search_postfix+str(page)
                    break
            else:
                complete = True
                break

    return codec.search_result[index]['href']


def direct():

    direct_question = {
        'type': 'input',
        'name': 'direct',
        'message': 'Enter the url: ',
    }

    answer = prompt(direct_question)

    return answer['direct']


def download_link(manga_url):
    while True:
        dm.print_info(manga_url)

        print("\nLeave following field empty to start from beginning chapter")
        manga_start = input('Start index: ')
        if manga_start == '':
            manga_start = 1

        ch_lst = None
        print("\nLeave following field empty to download till last chapter")
        manga_end = input('End index: ')
        if manga_end == '':
            ch_lst = dm.get_chapter_list(manga_url)
            manga_end = len(ch_lst)

        if manga_url[-1] == '/':
            manga_url = manga_url[0:-1]

        try:
            int_start = int(manga_start)
            int_end = int(manga_end) + 1
            break
        except ValueError:
            print('Start or end chapter numbers not numerical')

    dm.download_manga(manga_url, int_start, int_end, ch_lst)


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
            print('[SETTING] %s set to %s' %
                  (key.capitalize(), str(dmanager.settings[key])))

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

    if composite_answer['make_composites'] == True:
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
    elif composite_answer['make_composites'] == False:
        make_composites = False
        keep_originals = True
        composition_type = 'pdf'
        print('Keep_originals: True')

    dm.save_settings(make_composites, keep_originals, composition_type)


def check_files(download_manager):
    '''
    Checks for existance of neccesary files
    '''
    if not os.path.exists(Const.StyleSaveFile):
        list_to_file(style, Const.StyleSaveFile)
    if not download_manager.settings_exists():
        settings(download_manager)
    else:
        if not download_manager.verify_settings():
            print('Imported settings unsupported')
            settings(download_manager, skip_check=True)


if __name__ == '__main__':
    dm = MangaDownloader()
    codec = MKCodec()
    manga_manager = MangaManager()
    html_manager = HtmlManager()

    check_files(dm)

    while True:
        mainmenu = {
            'type': 'list',
            'name': 'menu',
            'message': 'what do you wanna do?',
            'choices': [
                'Search for manga',
                'Open manga using direct url',
                'View the manga',
                Separator(),
                'Settings',
                'Exit'
            ],
            'filter': lambda val: mainmenu['choices'].index(val),
            'default': 4

        }

        menuoption = prompt(mainmenu)

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
            # View
            manga_manager.generate_tree()
            html_manager.generate_web(manga_manager.tree)
            if(html_manager.open()):
                break
        elif menuoption['menu'] == 4:
            settings(dm)
        elif menuoption['menu'] == 5:
            break
        else:
            print('Pick a valid choice')
