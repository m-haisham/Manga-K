from modules.ui.colorize import red, green, blue
from .unicode import CHECK_MARK


class Completer:
    def __init__(self, s: str):
        if type(s) != str:
            raise TypeError('"s" must be of type str')

        self.message = s

    def init(self):
        print(f'\r[ ] {self.message}', end='')
        return self

    def complete(self):
        if self._done:
            raise ValueError('this bar has already ran to completion')
        self._done = True

        print(f'\r[{green(CHECK_MARK)}] {self.message}')

    def fail(self, s=''):
        if self._done:
            raise ValueError('this bar has already ran to completion')
        self._done = True

        print(f'\r[{red("X")}] {self.message}')

        if type(s) != str:
            raise TypeError('"s" must be of type str')
        if s != '':
            print(f'[{blue("!")}] {s}')

    def __str__(self):
        return self.message

    def __enter__(self):
        return self.init();

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._done:
            self.complete()