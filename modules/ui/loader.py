import threading
import time

from .completer import Completer


class Loader:
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

    def __init__(self, func, s, *args, **kwargs):

        if type(s) != str:
            raise TypeError('"s" must be of type str')

        self.message = s

        self.thread = threading.Thread(target=lambda: func(*args, **kwargs))
        self.thread.daemon = True

    def run(self) -> None:
        # start thread
        self.thread.start()

        index = 0
        while True:
            print(f'\r[{self.STATES[index]}] {self.message}', end='')

            if not self.thread.is_alive():
                Completer(f'{self.message}    ').init().complete()
                break

            time.sleep(0.3)
            index = (index + 1) % len(self.STATES)
