from modules.MangaDownloader import MangaDownloader
from modules.codec import MKCodec
from modules.manager import MangaManager, HtmlManager
import os

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

def settings(dmanager):
    if dmanager.settings_exists():
        print('- - - Settings - - -')
        dmanager.load_settings()
        print('Make Composite: '+str(dmanager.settings['make_composite']))
        print('Keep Originals: '+str(dmanager.settings['keep_originals']))

        while True:
            make_settings = input("Change Settings (Y/N): ")
            if make_settings.lower() == 'y':
                make_settings = True
                break
            elif make_settings.lower() == 'n':
                make_settings = False
                break
            else:
                print('pick a valid choice')
        if not make_settings:
            return
    else:
        print('No Settings Saved')

    while True:
        make_composites = input("\nMake Composites (Y/N): ")
        if make_composites.lower() == 'y':
            make_composites = True
            while True:
                keep_originals = input("Keep originals (Y/N): ")
                if keep_originals.lower() == 'y':
                    keep_originals = False
                    break
                elif keep_originals.lower() == 'n':
                    keep_originals = True
                    break
                else:
                    print('pick a valid choice')
            break
        elif make_composites.lower() == 'n':
            make_composites = False
            keep_originals = True
            print('Keep_originals: True')
            break
        else:
            print('pick a valid choice')
    dm.save_settings(make_composites, keep_originals)


if __name__ == '__main__':
    dm = MangaDownloader()
    codec = MKCodec()
    manga_manager = MangaManager()
    html_manager = HtmlManager()

    if not dm.settings_exists():
        settings(dm)
    
    print('- - - Manga K - - -')
    print('')
    print('1. Search')
    print('2. Direct URL')
    print('3. View')
    print('4. Settings')
    print('5. Exit')
    while True:
        res = input('\n//> ')

        if res == '1':
            download_link(search())
        elif res == '2':
            download_link(direct())
        elif res == '3':
            manga_manager.generate_tree()
            html_manager.generate_web(manga_manager.tree)
            html_manager.open()
            break
        elif res == '4':
            settings(dm)
        elif res == '5':
            break
        else:
            print('Pick a valid choice')