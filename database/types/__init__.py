import json
from pathlib import Path

from sqlalchemy import TypeDecorator, String


class ArrayType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return ArrayType(self.impl.length)


class PathType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return Path(value)

    def copy(self):
        return PathType(self.impl.length)
