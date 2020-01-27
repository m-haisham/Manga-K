import re

from .decorators import Suppress


def validate(s, dot=True):
    s = re.sub('[^A-Za-z0-9 -.]+', '', s)
    s = re.sub("\s\s+", " ", s)

    if dot:
        s = ''.join(s.split('.'))

    return s.strip()


def validate_list(l, key=None):
    if key is None:
        key = lambda v: validate(v)

    return [key(item) for item in l]
