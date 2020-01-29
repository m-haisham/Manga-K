from pathlib import Path
from .key import KeyDB


class Mangabase(KeyDB):
    instance = None

    def __init__(self, *args, **kwargs):
        super(Mangabase, self).__init__(*args, **kwargs)

        self.map = self.table('map')


def get():
    """
    instantiates database if it doesnt already exist

    :return: main instance of mangabase database
    """
    if Mangabase.instance is None:
        Mangabase.instance = Mangabase(Path('data') / Path('manga.db'))

    return Mangabase.instance
