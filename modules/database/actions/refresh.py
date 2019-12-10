from tinydb import Query

from modules.codec import MKCodec
from modules.console import vinput, title, visualize
from modules.database.models import Chapter
from modules.ui import Loader
from ..mangas import base, add_manga, manga as mangabase
from ..models import Manga


def refresh():
    unsuccessful = mangas_check()
    while len(unsuccessful) > 0:
        manual(unsuccessful)

        print(title('Rechecking mangas'))
        unsuccessful = mangas_check()

    unsuccessful = chapters_check(base.all())
    while len(unsuccessful) > 0:
        # prompt for manual url insertion
        manual(unsuccessful)

        print(title('Rechecking chapters'))
        unsuccessful = chapters_check(base.all())

    print()

def mangas_check():
    unsuccessful_retrievals = []
    with Loader('Getting started') as loader:
        for manga in Manga.directory.iterdir():
            manga = Manga(manga.parts[-1], '')

            url = ''

            loader.message = f'try to get {manga.title} url from database'
            result = base.search(Query().title == manga.title)
            if len(result) > 0 and result[0]['url'] != '':
                url = result[0]['url']
            else:
                loader.message = f'try to get {manga.title} url from online'
                try:
                    codec = MKCodec()

                    codec.search(codec.search_prefix + manga.title)

                    if len(codec.search_result) > 0:
                        url = codec.search_result[0]['href']
                except Exception as e:
                    loader.print(e)
                    url = ''

            manga.url = url
            if url != '':
                # update database
                add_manga(manga.title, url, manga.path())
            else:
                unsuccessful_retrievals.append(manga)

        loader.message = 'Manga check'
        if len(unsuccessful_retrievals) > 0:
            loader.fail(f'information retrieval of {len(unsuccessful_retrievals)} unsuccessful')

    return unsuccessful_retrievals


def chapters_check(manga_list):
    unsuccessful_retrievals = []
    with Loader('Chapter check') as loader:
        # for all manga get list of downloaded chapters
        for obj in manga_list:
            manga = Manga.fromdict(obj)

            loader.message = f'Checking {manga.title}'

            manga, chapter_list = manga.parse()

            try:
                mangabase.databases[manga.title].update_chapter_list(chapter_list)
            except KeyError:
                unsuccessful_retrievals.append(manga)
                continue

            try:
                chapter_directories = list(manga.path().iterdir())
            except FileNotFoundError:
                # file is in database but not in filesystem, so entry is being removed
                loader.print(f'[{visualize(False)}] {manga.title} NotFound: Removed from database')
                base.remove(Query().url == manga.url)

            # for each chapter in file system
            for cpath in chapter_directories:
                chapter = Chapter(cpath.parts[-1], '')

                filtered = list(filter(lambda val: val.title == chapter.title, chapter_list))
                if len(filtered) <= 0:
                    continue

                # title based update
                mangabase.databases[manga.title].chapters.update({'downloaded': True}, Query().url == filtered[0].url)

        loader.message = 'Chapter check'
        if len(unsuccessful_retrievals) > 0:
            loader.fail(f'information retrieval of {len(unsuccessful_retrievals)} unsuccessful')

    return unsuccessful_retrievals


def manual(manga_list):
    print()
    print(title('Switching to manual url insertion'))
    for manga in manga_list:
        print(title(manga.title))
        manga.url = vinput('Enter url')

        add_manga(manga.title, manga.url, manga.path())
