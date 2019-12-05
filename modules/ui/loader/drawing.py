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

        self.error = False
        self.drawing_speed = 0.1
        self._stop_event = threading.Event()

        self.index = 0

    def stop(self, error=False):
        self._stop_event.set()
        self.error = error

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def set_message(self, message):
        self.message = message

        delete_line()
        print(f'\r{self.state.states[self.index]} {self.message}', end='')

    def run(self) -> None:

        # making sure it is with in limit
        self.index = self.index % len(self.state.states)

        while True:
            print(f'\r{self.state.states[self.index]} {self.message}', end='')

            if self.stopped():
                delete_line()
                c = Completer(f'{self.message}', self.state.to_completer_state()).init()
                if not self.error:
                    c.complete()
                else:
                    c.fail()
                return

            time.sleep(self.drawing_speed)
            self.index = (self.index + 1) % len(self.state.states)
