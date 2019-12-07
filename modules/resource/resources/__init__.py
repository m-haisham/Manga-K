from pathlib import Path

from .default import Resource


class RawResource(Resource):
    def __init__(self, data, path: Path):
        self.data = data

        if type(path) == str:
            self.path = Path(path).absolute()
        else:
            self.path = path.absolute()

    def check(self):
        return self.path.exists()

    def make(self, check=True):
        if check and self.check():
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)

        if type(self.data) == str:
            with self.path.open('w') as f:
                f.write(self.data)
