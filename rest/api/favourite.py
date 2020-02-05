from flask_restful import Resource

from database.access import MangaAccess
from database.schema import mangas_schema


class FavouriteList(Resource):
    def get(self):
        favourites = MangaAccess.filter(favourite=True)

        return mangas_schema.dump(favourites)
