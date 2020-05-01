from flask_restful import Resource

from database.access import MangaAccess
from database.schema import mangas_schema


class FavouriteList(Resource):
    def get(self):
        favourites = MangaAccess.filter(favourite=True)

        f_dicts = mangas_schema.dump(favourites)
        for i, favourite in enumerate(favourites):
            f_dicts[i]['updates'] = len([chapter for chapter in favourite.chapters if chapter.update_status])

        return f_dicts
