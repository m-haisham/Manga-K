import re

from .decorators import Suppress


def validate(s, dot=True):
    s = re.sub('[^A-Za-z0-9 -.]+', '', s)
    s = re.sub("\s\s+", " ", s)

    if dot:
        s = ''.join(s.split('.'))

    return s.strip()
