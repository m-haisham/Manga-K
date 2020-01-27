
from ..exceptions import IdentificationError

class Manga:
    def __init__(self):

        self.title = ''
        self.status = Status.UNKNOWN
        self.description = ''
        self.url = ''


class Status:
    UNKNOWN = 'unknown'
    ONGOING = 'ongoing'
    COMPLETE = 'complete'

    @staticmethod
    def parse(s):
        _s = s.lower()

        if _s == Status.UNKNOWN:
            return Status.UNKNOWN
        elif _s == Status.ONGOING:
            return Status.ONGOING
        elif _s == Status.COMPLETE:
            return Status.COMPLETE
        else:
            raise IdentificationError('Unable to identify status.')