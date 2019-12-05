from modules.ui.loader.state import State
from ..item import UItem
from .drawing import DrawingThread


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

    def __init__(self, s, state=State(5)):
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

    def fail(self):
        super().fail()

        # stop drawing
        self.thread.stop(error=True)

        # sanity check
        while self.thread.is_alive():
            pass
