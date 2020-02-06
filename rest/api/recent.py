from flask_restful import Resource

from database import LocalSession
from database.access import RecentsAccess
from database.models import RecentModel
from database.schema import recents_schema


class RecentList(Resource):
    def get(self):
        """
        :return: all recents
        """
        recents = LocalSession.session.query(RecentModel).all()

        return recents_schema.dump(recents)