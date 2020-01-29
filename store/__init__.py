"""
Path is referred as filesystem paths
"""
import re
from pathlib import Path

BASE_PATH = Path('static')


def manga_path(manga_title):
    """
    :param manga_title: title of manga
    :return: filesystem save path of manga
    """
    return BASE_PATH / Path(slugify(manga_title))


def chapter_path(manga_title, chapter_title):
    """
    :param manga_title: title of manga
    :param chapter_title: title of chapter
    :return: filesystem sae path of chapter
    """
    return BASE_PATH / Path(slugify(manga_title)) / Path(slugify(chapter_title))


def sanitize(d):
    del d['path']
    return d


def slugify(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
