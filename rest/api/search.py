from flask_api import status
from flask_restful import Resource, reqparse

from database import LocalSession
from database.access import ThumbnailAccess, MangaAccess
from database.models import MangaModel
from database.models.thumbnail import Thumbnail
from database.schema import discover_schema
from network.scrapers import Mangakakalot
from rest.error import error_message

parser = reqparse.RequestParser()
parser.add_argument('word')


class Search(Resource):
    def post(self, i):
        args = parser.parse_args()

        mangakakalot = Mangakakalot()
        mangas = mangakakalot.get_search(args['word'], i)

        if mangas is None:
            return error_message(f'Latest at index {i} not found'), status.HTTP_404_NOT_FOUND

        models = []
        for manga in mangas:
            # Arrange
            manga_model = MangaModel.from_manga(manga)

            # Insert and modify
            access, inserted = MangaAccess.gesert(manga_model)
            if not inserted:
                # update and persist
                manga_model = access.update(**vars(manga))

            thumbnail = Thumbnail(manga_model)
            ThumbnailAccess.upsert(thumbnail, commit=False)

            models.append(manga_model)

        LocalSession.session.commit()

        return discover_schema.dump(models)
