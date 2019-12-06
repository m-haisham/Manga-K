import collections


class Runnable:
    def __init__(self, func):

        if not isinstance(func, collections.Callable):
            raise TypeError('func must be a callable')

        self.func = func

    def run(self, *args, **kwargs):
        return self.func(*args, **kwargs)