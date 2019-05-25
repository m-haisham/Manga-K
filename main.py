from MangaDownloader import MangaDownloader
import os

if __name__ == '__main__':
    dm = MangaDownloader()
    save_file_exists = os.path.exists(dm.settings_path)
    while(True):
        manga_url = input('Input full url to manga from mangakakalot.com|manganel.com\nURl: ')

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

        if save_file_exists:
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

        if save_file_exists and not make_settings:
            dm.load_settings()
        else:        
            while True:
                make_composites = input("\nMake Composites (Y/N): ")
                if make_composites.lower() == 'y':
                    make_composites = True
                    while True:
                        keep_originals = input("Delete originals (Y/N): ")
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
                    break
                else:
                    print('pick a valid choice')
            dm.save_settings(make_composites, keep_originals)
        
        try:
            int_start = int(manga_start)
            int_end = int(manga_end) + 1
            break
        except ValueError:
            print('Start or end chapter numbers not numerical')

    dm.download_manga(manga_url, int_start, int_end, ch_lst)
