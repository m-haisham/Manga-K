from .colorize import red, green, blue
from .item import UItem
from .unicode import CHECK_MARK


class Completer(UItem):
    def init(self):
        print(f'\r[ ] {self.message}', end='')
        return self

    def complete(self):
        super().complete()

        print(f'\r[{green(CHECK_MARK)}] {self.message}')

    def fail(self, s=''):
        super().fail()

        print(f'\r[{red("X")}] {self.message}')

        if type(s) != str:
            raise TypeError('"s" must be of type str')
        if s != '':
            print(f'[{blue("!")}] {s}')

    def __str__(self):
        return self.message