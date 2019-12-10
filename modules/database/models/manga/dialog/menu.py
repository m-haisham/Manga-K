from modules import favourite
from modules.console.menu import Menu
from modules.database.mangas import update_is_manhwa
from ..manga import Manga


class MangaDialog:
    def __init__(self, manga: Manga, chapters=None):
        self.manga = manga
        self.chapters = chapters

        self.options = {}

        self.menu = Menu('Pick an action', self.options)

        self._construct_menu()

    def prompt(self):
        while True:
            try:
                r = self.menu.prompt()
            except KeyError as e:
                break

            if r:
                break

            # reconstruct to deal with changed settings
            self._construct_menu()

    def repeat(self, func, *args, **kwargs):
        func(*args, **kwargs)
        return True

    def _construct_menu(self):
        self.options = {}

        if not favourite.exist(self.manga):
            self.options['Add to favourites'] = lambda: self.repeat(favourite.upsert, self.manga)

        from ..download import select_and_download
        self.options['Download'] = lambda: select_and_download(self.manga, self.chapters)

        self.options[f'[{self.manga.is_manhwa}] Set Manhwa to {not self.manga.is_manhwa}'] = self._toggle

        if favourite.exist(self.manga):
            self.options['Remove from favourites'] = lambda: self.repeat(favourite.remove, self.manga)

        self.menu = Menu('Pick an action', self.options)

    def _toggle(self):
        update_is_manhwa(self.manga, not self.manga.is_manhwa)
        self.manga.is_manhwa = not self.manga.is_manhwa
