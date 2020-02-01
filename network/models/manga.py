from ..exceptions import IdentificationError


class Manga:
    def __init__(self):
        self.title = ''
        self.status = Status.UNKNOWN
        self.description = ''
        self.genres = []
        self.url = ''
        self.thumbnail_url = ''


class Status:
    UNKNOWN = 'unknown'
    ONGOING = 'ongoing'
    COMPLETE = 'completed'

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
