from pathlib import Path

from tinydb import Query

from modules.database.manga import MangaData
from modules.database.paths import base_path
from modules.database.wrapper import TinyWrapper

base = TinyWrapper(base_path)
mangadata = MangaData(base)

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
        base.insert({'title': title, 'url': url, 'path': path, 'is_manhwa': False})

    mangadata.add(title)


def update_is_manhwa(_manga, state):
    base.upsert(dict(is_manhwa=state), Query().url == _manga.url)
    mangadata.databases[_manga.title].update_info({'is_manhwa': state})

    from modules import favourite
    favourite.update(_manga, {'is_manhwa': state})
