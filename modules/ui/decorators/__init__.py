from ..completer import Completer as CompleterClass
from ...ui import Loader as LoaderClass
from ..loader import State
from ..completer import CompleterType

class Completer:
    def __init__(self, message, ctype=CompleterType()):
        self.message = message
        self.ctype = ctype

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            c = CompleterClass(self.message, self.ctype).init()
            try:
                r = func(*args, **kwargs)
            except Exception as e:
                c.fail(e)
                raise e

            c.complete()
            return r

        return wrapper


class Loader:
    def __init__(self, message, state=State(5)):
        self.message = message
        self.state = state

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            l = LoaderClass(self.message, self.state).init()
            try:
                r = func(*args, **kwargs)
            except Exception as e:
                l.fail(e)
                raise e

            l.complete()

            return r

        return wrapper
