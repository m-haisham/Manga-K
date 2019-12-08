from typing import List

from tinydb import Query

from ..database.database import meta
from ..database.models import Manga

favourite = Query()


def upsert(manga: Manga):
    """
    Add to favourites
    :param manga: manga object to be added
    :return:
    """
    meta.favourites.upsert(manga.todict(), favourite.url == manga.url)


def remove(manga: Manga):
    """
    Remove from favourites
    :param manga: manga object to be removed
    :return:
    """
    meta.favourites.remove(favourite.url == manga.url)


def exist(manga: Manga) -> bool:
    """
    checks whether the given manga is in favourites
    :param manga: manga object to be tested
    :return: True if exist anf False otherwise
    """
    l = meta.favourites.search(favourite.url == manga.url)
    if len(l) > 0:
        return True
    else:
        return False


def all() -> List[Manga]:
    """
    :return: list of favoured manga objects
    """
    return [Manga.fromdict(doc) for doc in meta.favourites.all()]
