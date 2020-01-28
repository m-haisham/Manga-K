from pathlib import Path
from .key import KeyDB


class Mainbase(KeyDB):
    instance = None

    def __init__(self, *args, **kwargs):
        super(Mainbase, self).__init__(*args, **kwargs)

        self.settings = self.table('')
        self.recents = self.table('recents')


def get():
    """
    instantiates database if it doesnt already exist

    :return: main instance of mainbase database
    """
    if Mainbase.instance is None:
        Mainbase.instance = Mainbase(Path('data') / Path('data.db'))

    return Mainbase.instance
