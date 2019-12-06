from pathlib import Path

from tinydb import Query

from .manga import MangaData
from .paths import base_path, meta_path
from .wrapper import TinyWrapper, MetaWrapper

# databases
base = TinyWrapper(base_path)
meta = MetaWrapper(meta_path)
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
    base.upsert({'title': title, 'url': url, 'path': path}, query.title == title)
    manga.add(title)
