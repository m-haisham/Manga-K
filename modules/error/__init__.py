import re

from .decorators import Suppress


def validate(s):
    s = re.sub('[^A-Za-z0-9 -.]+', '', s)
    s = ''.join(s.split('.'))
    s = re.sub("\s\s+", " ", s)
    return s.strip()
