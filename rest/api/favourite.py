from flask_restful import Resource

from database.access import MangaAccess


class FavouriteList(Resource):
    def get(self):
        all_mangas = [MangaAccess(title).get_info(recorded=False) for title in MangaAccess.all()]

        favourites = filter(lambda info: info is not None and info['favourite'], all_mangas)
        return list(favourites)
