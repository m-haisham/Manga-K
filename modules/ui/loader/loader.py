from modules.ui.loader.style import LoaderStyle
from .drawing import DrawingThread
from ..item import UItem


class Loader(UItem):
    """
    an indefinite loader

    change message mid execution to change display hint

    use
    with Loader(msg) as l:

        # to show fail
        l.fail(*optional_msg)

    or use decorators for functions
    """

    def __init__(self, s, state=LoaderStyle(5)):
        super().__init__(s)

        self.thread = DrawingThread(message=s, state=state)
        self.thread.daemon = True

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, val):
        self.thread.set_message(val)
        self._message = val

    def set_drawing_speed(self, speed):
        self.thread.drawing_speed = speed

    def init(self):
        # start drawing
        self.thread.start()

        return self

    def complete(self):
        super().complete()

        # stop drawing
        self.thread.stop(error=False)

        # sanity check
        while self.thread.is_alive():
            pass

    def fail(self, error=''):
        super().fail()

        # stop drawing
        self.thread.stop(error=error)

        # sanity check
        while self.thread.is_alive():
            pass
