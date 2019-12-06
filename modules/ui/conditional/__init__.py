from ..completer import Completer
from ..loader import Loader, LoaderStyle
from ..runnable import Runnable


class ConditionalCompleter(Completer):
    def __init__(self, s: str, condition: bool):
        super().__init__(s)

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
