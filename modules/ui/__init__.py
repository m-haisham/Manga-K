from .completer import Completer, CompleterStyle
from .loader import Loader, DrawingThread, LoaderStyle
from .runnable import Runnable


class RunnableCompleter(Runnable):
    def __init__(self, func, message, style=CompleterStyle(), condition=True):
        super().__init__(func)
        self.message = message
        self.style = style
        self.condition = condition

    def run(self, *args, **kwargs):
        if self.condition:
            c = Completer(self.message, self.style).init()
            try:
                output = super().run(*args, **kwargs)
            except Exception as e:
                c.fail(e)
                raise e

            c.complete()

            return output
        else:
            return super().run(*args, **kwargs)


class RunnableLoader(Runnable):
    def __init__(self, func, message, style=LoaderStyle(5), condition=True):
        super().__init__(func)
        self.message = message
        self.style = style
        self.condition = condition

    def run(self, *args, **kwargs):
        if self.condition:
            l = Loader(self.message, self.style).init()
            try:
                output = super().run(*args, **kwargs)
            except Exception as e:
                l.fail(e)
                raise e

            l.complete()

            return output
        else:
            return super().run(*args, **kwargs)
