from tinydb import TinyDB

class TinyWrapper(TinyDB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = args[0]