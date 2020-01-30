"""
Links are referred as server paths
"""

from store import slugify


def manga_link(manga_title):
    return f'/manga/{slugify(manga_title)}'


def chapter_link(manga_title, chapter_title):
    return f'/manga/{slugify(manga_title)}/{slugify(chapter_title)}'


def page_link(manga_title, chapter_title, page_number):
    return f'/manga/{slugify(manga_title)}/{slugify(chapter_title)}/{page_number}'
