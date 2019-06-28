import os
import traceback

from modules.codec import MKCodec
from modules.conversions import create_py_list, list_to_file
from modules.manager import HtmlManager, MangaManager
from modules.MangaDownloader import MangaDownloader
from modules.static import Const
from modules.styles import style

def search():
    search = input('Enter here to search: ')
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
                        url = codec.search_prefix+search+codec.search_postfix+str(page)
                    break
            else:
                complete = True
                break

    return codec.search_result[index]['href']

def direct():
    return input('Input full url to manga from mangakakalot.com|manganel.com\nURl: ')
    
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

def settings(dmanager, skip_check = False):
    if not skip_check and dmanager.settings_exists():
        # load save file
        dmanager.load_settings()

        # load settings
        settings_keys = dmanager.settings.keys()

        # print page title to console
        print('- - - Settings - - -')

        # print settings to console
        for key in settings_keys:
            print('[SETTING] [%s] set to %s' % (key.upper(), str(dmanager.settings[key])))

        # ask whether to change settings
        while True:
            make_settings = input("Change Settings (Y/N): ")
            if make_settings.lower() == 'y':
                make_settings = True
            elif make_settings.lower() == 'n':
                make_settings = False
            else:
                print('pick a valid choice')
                continue
            break
        # exit function, not changing settings
        if not make_settings:
            return
    # no settings saved or promted to skip, run rest of function
    else:
        if not skip_check:
            print('No Settings Saved')

    # create settings
    while True:
        # whether to make composites
        make_composites = input("\nMake Composites (Y/N): ")
        if make_composites.lower() == 'y':
            make_composites = True
            # which composition type
            while True:
                print('Composition types')
                print('1: pdf')
                print('2: jpg')
                composition_index = input('Pick type: ')
                if composition_index == '1':
                    composition_type = 'pdf'
                elif composition_index == '2':
                    composition_type = 'image'
                else:
                    print('pick a valid choice')
                    continue
                break
            # whether to keep seperate images
            while True:
                keep_originals = input("Keep originals (Y/N): ")
                if keep_originals.lower() == 'y':
                    keep_originals = True
                elif keep_originals.lower() == 'n':
                    keep_originals = False
                else:
                    print('pick a valid choice')
                    continue
                break
            break
        # default rest of settings
        elif make_composites.lower() == 'n':
            make_composites = False
            keep_originals = True
            composition_type = 'pdf'
            print('Keep_originals: True')
            break
        else:
            print('pick a valid choice')
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
        print('- - - Manga K - - -')
        print('')
        print('1. Search')
        print('2. Direct URL')
        print('3. View')
        print('4. Settings')
        print('5. Exit')
        res = input('\n//> ')

        if res == '1':
            try:
                download_link(search())
            except Exception:
                traceback.print_exc()
        elif res == '2':
            try:
                download_link(direct())
            except Exception:
                traceback.print_exc()
        elif res == '3':
            # View
            manga_manager.generate_tree()
            html_manager.generate_web(manga_manager.tree)
            if(html_manager.open()):
                break
        elif res == '4':
            settings(dm)
        elif res == '5':
            break
        else:
            print('Pick a valid choice')
