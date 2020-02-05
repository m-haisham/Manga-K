from flask_restful import Resource

from database.access import RecentsAccess


class RecentList(Resource):
    def get(self):
        """
        :return: all recents
        """
        # arrange
        recents = RecentsAccess().all()
        for recent in recents:
            del recent['pages']
            del recent['thumbnail_path']

        return recents