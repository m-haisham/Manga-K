from threading import Lock


class AtomicBoolean:
    def __init__(self, value):
        self._value = value
        self._lock = Lock()

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, v):
        with self._lock:
            self._value = v
