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
        print(f'\r[{green(CHECK_MARK)}] {self.message}')

    def fail(self, s=''):
        print(f'\r[{red("X")}] {self.message}')

        if type(s) != str:
            raise TypeError('"s" must be of type str')
        if s != '':
            print(f'[{blue("!")}] {s}')

    def __str__(self):
        return self.message
