import threading
import time

from .completer import Completer
from .item import UItem

class DrawingThread(threading.Thread):
    """Thread class that draws indefinitely until stoppped"""

    def __init__(self, message='', *args, **kwargs):
        super(DrawingThread, self).__init__(*args, **kwargs)
        self.message = message
        self.error = False
        self.drawing_speed = 0.1
        self._stop_event = threading.Event()

    def stop(self, error = False):
        self._stop_event.set()
        self.error = error

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self) -> None:
        index = 0
        while True:
            print(f'\r[{Loader.STATES[index]}] {self.message}', end='')

            if self.stopped():
                c = Completer(f'{self.message}    ').init()
                if not self.error:
                    c.complete()
                else:
                    c.fail()
                return

            time.sleep(0.1)
            index = (index + 1) % len(Loader.STATES)


class Loader(UItem):
    FULL_BLOCK = '\u2588'
    EMPTY_SPACE = ' '

    CLEAR_LINE = "\033[K"

    STATES = [
        (EMPTY_SPACE * 0) + (FULL_BLOCK * 1) + (EMPTY_SPACE * 4),
        (EMPTY_SPACE * 0) + (FULL_BLOCK * 2) + (EMPTY_SPACE * 3),
        (EMPTY_SPACE * 0) + (FULL_BLOCK * 3) + (EMPTY_SPACE * 2),
        (EMPTY_SPACE * 0) + (FULL_BLOCK * 4) + (EMPTY_SPACE * 1),
        (EMPTY_SPACE * 0) + (FULL_BLOCK * 5) + (EMPTY_SPACE * 0),
        (EMPTY_SPACE * 1) + (FULL_BLOCK * 4) + (EMPTY_SPACE * 0),
        (EMPTY_SPACE * 2) + (FULL_BLOCK * 3) + (EMPTY_SPACE * 0),
        (EMPTY_SPACE * 3) + (FULL_BLOCK * 2) + (EMPTY_SPACE * 0),
        (EMPTY_SPACE * 4) + (FULL_BLOCK * 1) + (EMPTY_SPACE * 0),
        (EMPTY_SPACE * 5) + (FULL_BLOCK * 0) + (EMPTY_SPACE * 0),
    ]

    def __init__(self, s):
        super().__init__(s)

        self.thread = DrawingThread(message=s)
        self.thread.daemon = True


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