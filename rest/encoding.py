"""
Links are referred as server paths
"""

from store import slugify


def manga_link(manga_title):
    return f'/manga/{slugify(manga_title)}'


def chapter_link(manga_title, chapter_title):
    return f'/manga/{slugify(manga_title)}/{slugify(chapter_title)}'


def page_link(manga_id, chapter_id, page_number):
    return f'/page/{manga_id}/{chapter_id}/{page_number}'


def thumbnail_link(manga_title):
    return f'/manga/{slugify(manga_title)}/thumbnail'
