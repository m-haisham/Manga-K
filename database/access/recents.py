from datetime import datetime

from database import LocalSession
from database.models import RecentModel


class RecentsAccess:

    @staticmethod
    def upsert(recent, commit=True):
        """
        Adds model to recents
        Non repeating

        :param recent_model: model to add
        :return: None
        """
        old = LocalSession.session.query(RecentModel).filter_by(manga_id=recent.manga_id).first()
        if old is None:
            LocalSession.session.add(recent)
        else:
            old.chapter_id = recent.chapter_id
            old.time = datetime.utcnow()
            recent = old

        if commit:
            LocalSession.session.commit()

        return recent

    @staticmethod
    def all():
        """
        :return: all recents
        """
        pass
