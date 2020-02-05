"""
Path is referred as filesystem paths
"""
import re
from pathlib import Path

from .decorators import mkdir

BASE_PATH = Path('static')


def manga_path(manga_title) -> Path:
    """
    :param manga_title: title of manga
    :return: filesystem save thumbnail_path of manga
    """
    return BASE_PATH / Path(slugify(manga_title))


def chapter_path(manga_title, chapter_title) -> Path:
    """
    :param manga_title: title of manga
    :param chapter_title: title of chapter
    :return: filesystem save thumbnail_path of chapter
    """
    return BASE_PATH / Path(slugify(manga_title)) / Path(slugify(chapter_title))


def sanitize(d: dict) -> dict:
    del d['thumbnail_path']
    return d


def slugify(s: str) -> str:
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)  # TEST .lower()
