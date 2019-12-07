from pathlib import Path

from .default import Resource


class RawResource(Resource):
    def __init__(self, data, path: Path):
        self.data = data

        if type(path) != Path:
            self.path = Path(path)
        elif type(path) != Path:
            self.path = path
        else:
            raise TypeError('path must be a str or Path')

    def check(self):
        return self.path.exists()

    def make(self, check=True):
        if check and self.check():
            return

        self.path.parent.mkdir(parent=True, exists_ok=True)

        if type(self.data) == str:
            with self.path.open('w') as f:
                f.write(self.data)
