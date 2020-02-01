from pathlib import Path
from .key import KeyDB


class Mainbase(KeyDB):
    instance = None

    def __init__(self, *args, **kwargs):
        super(Mainbase, self).__init__(*args, **kwargs)

        self.downloads = self.table('downloads', cache_size=100)
        self.thumbnail = self.table('thumbnail')
        self.recents = self.table('recents', cache_size=50)


def get():
    """
    instantiates database if it doesnt already exist

    :return: main instance of mainbase database
    """
    if Mainbase.instance is None:
        Mainbase.instance = Mainbase(Path('data') / Path('data.db'))

    return Mainbase.instance
