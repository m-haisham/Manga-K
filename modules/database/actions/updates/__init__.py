from modules import favourite
from modules.ui import Loader

from modules.database.mangas import mangadata
from .menu import UpdatesMenu
from modules.console import title

def updates():
    favoured = favourite.all()

    updates = {}
    with Loader("Initialize") as loader:
        for f_manga in favoured:
            loader.message = f'Parsing {f_manga.title}'

            # a bit of sanity check
            if f_manga.title not in mangadata.databases.keys():
                continue

            d_database = mangadata.databases[f_manga.title].get_chapter_list()
            _, d_online = f_manga.parse()

            # compare
            if len(d_database) == len(d_online):
                continue

            d_urls = [chapter.url for chapter in d_database]
            for o_chapter in d_online:
                if o_chapter.url not in d_urls:

                    if f_manga not in updates.keys():
                        updates[f_manga] = []

                    updates[f_manga].append(o_chapter)

        loader.message = 'Update check'

    if not updates.keys():
        print(title('No updates.'))
        return

    UpdatesMenu(updates).prompt()