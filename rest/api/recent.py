from flask_restful import Resource

from database import LocalSession
from database.access import MangaAccess
from database.models import RecentModel, ChapterModel
from database.schema import recents_schema, manga_schema, chapter_schema


class RecentList(Resource):
    def get(self):
        """
        :return: all recents
        """
        recents = LocalSession.session.query(RecentModel).order_by(RecentModel.time.desc()).all()

        recently = []
        for recent in recents:
            manga_access = MangaAccess(recent.manga_id)
            manga = manga_access.get()
            chapter = LocalSession.session.query(ChapterModel).get(recent.chapter_id)

            if manga is None or chapter is None:
                LocalSession.session.remove(recent)
                continue

            recently.append({
                'manga': manga_schema.dump(manga),
                'chapter': chapter_schema.dump(chapter),
                'time': str(recent.time)
            })

        LocalSession.session.commit()

        return recently
