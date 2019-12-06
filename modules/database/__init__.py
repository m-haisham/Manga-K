from tinydb import TinyDB, Query
from pathlib import Path
from .paths import base_path, meta_path
from .manga import MangaData
from .wrapper import TinyWrapper, MetaWrapper

# databases
base = TinyWrapper(base_path)
meta_base = MetaWrapper(meta_path)
manga_base = MangaData(base)


def add(title, url, path):
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
    manga_base.add(title)

    print(base.all())
