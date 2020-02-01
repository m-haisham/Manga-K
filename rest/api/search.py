from flask_api import status
from flask_restful import Resource, reqparse

from database.access import ThumbnailAccess
from network.scrapers import Mangakakalot
from rest.encoding import manga_link, thumbnail_link
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

        popular = []
        for manga in mangas:
            d_manga = vars(manga)

            del d_manga['description']
            del d_manga['status']
            del d_manga['genres']

            d_manga['link'] = manga_link(manga.title)
            d_manga['thumbnail_link'] = thumbnail_link(manga.title)

            # set thumbnail
            ThumbnailAccess(manga.title, manga.thumbnail_url)

            popular.append(d_manga)

        return popular
