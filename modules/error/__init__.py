import re
from .decorators import Suppress

def validate(path):
    return re.sub('[^A-Za-z0-9 -.]+', '', path)