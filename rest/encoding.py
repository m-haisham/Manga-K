"""
Links are referred as server paths
"""

import re


class UrlEncoding:

    @staticmethod
    def forward(s):
        """
        inverse of UrlEncoding.back

        :return: removes whitespace in url :param s:
        """
        return re.sub(' ', '_', s)

    @staticmethod
    def back(s):
        """
        inverse of UrlEncoding.forward

        :return: removes _ to add whitespace in url :param s:
        """
        return re.sub('_', ' ', s)


def manga_linked(manga: dict):
    """
    :param manga: manga to add link to
    :return: dict with link added
    """
    d = manga.copy()
    d['link'] = f'/manga/{UrlEncoding.forward(manga["title"])}'
    return d


def manga_link(title):
    return f'/manga/{UrlEncoding.forward(title)}'


def chapter_link(manga_title, chapter_title):
    return f'/manga/{UrlEncoding.forward(manga_title)}/{UrlEncoding.forward(chapter_title)}'


def page_link(manga_title, chapter_title, page_number):
    return f'/manga/{UrlEncoding.forward(manga_title)}/{UrlEncoding.forward(chapter_title)}/{page_number}'
