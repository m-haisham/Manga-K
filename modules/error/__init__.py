import re

def validate(path):
    return re.sub('[^A-Za-z0-9 -.]+', '', path)