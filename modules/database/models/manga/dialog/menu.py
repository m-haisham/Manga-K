from modules import favourite
from modules.console.menu import Menu
from .selection import select_and_download
from ..manga import Manga


class MangaDialog:
    def __init__(self, manga: Manga):
        self.manga = manga

        self.options = {}

        self.menu = Menu('Pick an action', self.options)

        self._construct_menu()

    def prompt(self):
        while True:
            r = self.menu.prompt()
            if not self.options[r]():
                break

    def repeat(self, func, *args, **kwargs):
        func(*args, **kwargs)
        return True

    def _construct_menu(self):
        if not favourite.exist(self.manga):
            self.options['Add to favourites'] = lambda: self.repeat(favourite.upsert, self.manga)

        self.options['download'] = lambda: select_and_download(self.manga)

        if favourite.exist(self.manga):
            self.options['Remove from favourites'] = lambda: self.repeat(favourite.remove, self.manga)

        self.menu = Menu('Pick an action', self.options)
