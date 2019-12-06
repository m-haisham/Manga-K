from .style import CompleterStyle
from ..colorize import colored
from ..item import UItem
from ..unicode import CHECK_MARK


class Completer(UItem):
    """
    check box type completer

    use
    with Completer(msg) as c:

        # to show fail
        c.fail(*optional_msg)

    or use decorators for functions
    """
    def __init__(self, s: str, ctype=CompleterStyle()):
        super().__init__(s)
        self.type = ctype

    def init(self):
        print(f'\r{self.type.prefix} {self.type.postfix} {self.message}', end='')
        return self

    def complete(self):
        super().complete()

        print(f'\r{self.type.prefix}{colored(CHECK_MARK, self.type.success)}{self.type.postfix} {self.message}')

    def fail(self, s=''):
        super().fail()

        print(f'\r{self.type.prefix}{colored("X", self.type.error)}{self.type.postfix} {self.message}')

        if s != '':
            print(f'{self.type.prefix}{colored("!", self.type.info)}{self.type.postfix} {s}')

    def __str__(self):
        return self.message