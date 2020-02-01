from flask_api import status
from flask_restful import Resource

from database.access import ThumbnailAccess
from network.scrapers import Mangakakalot
from ..encoding import manga_link, thumbnail_link

from ..error import error_message


class Latest(Resource):
    def get(self, i=1):

        mangakakalot = Mangakakalot()
        mangas = mangakakalot.get_latest(i)

        if mangas is None:
            return error_message(f'Latest at index {i} not found'), status.HTTP_404_NOT_FOUND

        latest = []
        for manga in mangas:
            d_manga = vars(manga)

            del d_manga['description']
            del d_manga['status']

            d_manga['link'] = manga_link(manga.title)
            d_manga['thumbnail_link'] = thumbnail_link(manga.title)

            # set thumbnail
            ThumbnailAccess(manga.title, manga.thumbnail_url)

            latest.append(d_manga)

        return latest
