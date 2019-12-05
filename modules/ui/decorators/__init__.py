from ..completer import Completer as CompleterClass
from ..loader import Loader as LoaderClass


class Completer:
    def __init__(self, message):
        self.message = message

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            c = CompleterClass(self.message).init()
            try:
                r = func(*args, **kwargs)
            except Exception as e:
                c.fail(e)
                raise e

            c.complete()
            return r

        return wrapper


class Loader:
    def __init__(self, message):
        self.message = message

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            LoaderClass(func, self.message, *args, **kwargs).run()

        return wrapper
