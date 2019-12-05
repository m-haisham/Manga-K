CHECK_MARK = "\u2713"

from .completer import Completer
from .loader import Loader

def completer(func, message):
    def function_wrapper(*args, **kwargs):
        c = Completer(message).init()
        try:
            r = func(*args, **kwargs)
        except Exception as e:
            c.fail(e)
            raise e

        c.complete()

        return r

    return function_wrapper


def loader(func, message):
    def function_wrapper(*args, **kwargs):
        Loader(func, message, *args, **kwargs).run()

    return function_wrapper