from tinydb import Query

from database import mainbase
from database.models import RecentModel

_recent = Query()


class RecentsAccess:
    recents = mainbase.get().recents

    def add(self, recent_model: RecentModel):
        """
        Adds model to recents
        Non repeating

        :param recent_model: model to add
        :return: None
        """
        self.recents.upsert(recent_model.to_dict(), _recent.manga_title == recent_model.manga_title)

    def all(self):
        """
        :return: all recents
        """
        return self.recents.all()
