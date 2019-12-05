import threading
import time

from .state import State
from ..line import delete_line
from ..completer import Completer


class DrawingThread(threading.Thread):
    """Thread class that draws indefinitely until stoppped"""

    def __init__(self, message='', state=State(5), *args, **kwargs):
        super(DrawingThread, self).__init__(*args, **kwargs)

        self.state = state

        self.message = message
        self.message_changed = False

        self.error = False
        self.drawing_speed = 0.1
        self._stop_event = threading.Event()

    def stop(self, error=False):
        self._stop_event.set()
        self.error = error

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def set_message(self, message):
        self.message_changed = True
        self.message = message

    def run(self) -> None:
        index = 0
        while True:
            if self.message_changed:
                delete_line()
                self.message_changed = False

            print(f'\r{self.state.states[index]} {self.message}', end='')

            if self.stopped():
                delete_line()
                c = Completer(f'{self.message}').init()
                if not self.error:
                    c.complete()
                else:
                    c.fail()
                return

            time.sleep(0.1)
            index = (index + 1) % len(self.state.states)
