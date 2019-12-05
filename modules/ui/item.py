class UItem:
    def __init__(self, s: str):
        if type(s) != str:
            raise TypeError('"s" must be of type str')

        self._message = s
        self._done = False

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, val):
        self._message = val

    def init(self):
        raise NotImplementedError()

    def complete(self):
        if self._done:
            raise ValueError('this bar has already ran to completion')
        self._done = True

    def fail(self):
        if self._done:
            raise ValueError('this bar has already ran to completion')
        self._done = True

    def __enter__(self):
        return self.init();

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._done:
            self.complete()
