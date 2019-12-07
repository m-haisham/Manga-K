from tinydb import Query

from modules.database.database import meta


def new(manga, to_download):
    # delete all from downloads left
    meta.downloads_left.purge()

    # add manga info to download resume
    meta.insert_manga(manga)

    # add all new get_chapter_list to be downloaded
    meta.downloads_left.insert_multiple([chapter.todict() for chapter in to_download])


def get():
    unfinished = meta.downloads_left.search(Query().downloaded == False)
    manga = meta.get_manga()

    return manga, unfinished


def update(url, status=True):
    meta.downloads_left.update({'downloaded': status}, Query().url == url)
