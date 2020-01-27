import re


class UrlEncoding:

    @staticmethod
    def forward(s):
        return re.sub(' ', '_', s)

    @staticmethod
    def back(s):
        return re.sub('_', ' ', s)


def linked_dict(manga):
    d = vars(manga)
    d['link'] = f'/manga/{UrlEncoding.forward(manga.title)}'
    return d
