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
        l = Loader(message).init()
        try:
            r = func(*args, **kwargs)
        except Exception as e:
            l.fail(e)
            raise e

        l.complete()

        return r

    return function_wrapper

