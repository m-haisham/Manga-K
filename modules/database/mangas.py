from pathlib import Path

from tinydb import Query

from modules.database.manga import MangaData
from modules.database.paths import base_path
from modules.database.wrapper import TinyWrapper

base = TinyWrapper(base_path)
manga = MangaData(base)

def add_manga(title, url, path):
    """
    adds new manga to main database or updates existing
    :param title: title of manga
    :param url: url pointing to manga website
    :param path: path to manga
    :return: None
    """

    if type(title) != str:
        raise TypeError('"title" must be of type str')

    if type(url) != str:
        raise TypeError('"url" must be of type str')

    if isinstance(path, Path):
        path = str(path)
    elif type(path) == str:
        pass
    else:
        raise TypeError('"path" must be of type str or pathlib.Path')

    query = Query()
    l = base.search(query.title == title)
    if len(l) > 0:
        base.upsert({'title': title, 'url': url, 'path': path}, query.title == title)
    else:
        base.insert({'title': title, 'url': url, 'path': path, 'is_manhua': False})

    manga.add(title)


def update_is_manhua(_manga, state):
    base.upsert(dict(is_manhua=state), Query().url == _manga.url)
    manga.databases[_manga.title].update_info(dict(is_manhua=state))

    from modules import favourite
    favourite.update(_manga, dict(is_manhua=state))
