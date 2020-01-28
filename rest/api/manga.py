from flask_api import status
from flask_restful import Resource, reqparse

from database.access import MangaAccess
from database.models import MangaModel, ChapterModel
from network import NetworkHelper
from network.scrapers import Mangakakalot
from ..encoding import manga_linked, UrlEncoding, chapter_link

pref_parser = reqparse.RequestParser()
pref_parser.add_argument('manhwa', type=bool)
pref_parser.add_argument('favourite', type=bool)


class Manga(Resource):
    def get(self, title):
        title = UrlEncoding.back(title)
        access = MangaAccess(title)

        info = access.get_info()
        if info is None:
            access.purge()
            return dict(message=f'{title} not found'), status.HTTP_404_NOT_FOUND

        # update chapters
        if NetworkHelper.is_connected():
            mangakakalot = Mangakakalot()

            chapters = mangakakalot.get_chapter_list(MangaModel.from_json(info))
            models = [ChapterModel.from_chapter(chapter, link=chapter_link(info['title'], chapter.title)) for chapter in chapters]

            access.update_chapters(models)

        info['chapters'] = access.get_chapters()
        return info

    def post(self, title):
        args = pref_parser.parse_args()

        title = UrlEncoding.back(title)
        access = MangaAccess(title)

        manga = access.get_info()
        if manga is None:
            access.purge()
            return dict(message=f'{title} not found'), status.HTTP_404_NOT_FOUND

        for key, value in args.items():
            if value is not None:
                manga[key] = value

        access.set_info(manga)

        return manga


url_parser = reqparse.RequestParser()
url_parser.add_argument('url', type=str)


class MangaList(Resource):
    def get(self):
        return [MangaAccess(title).get_info(recorded=False) for title in MangaAccess.all()]

    def post(self):
        args = url_parser.parse_args()

        connected = NetworkHelper.is_connected()

        access = MangaAccess.url(args['url'])
        if access is not None:
            previous = access.get_info()

            # no internet connection, return previously saved
            if not connected and previous is not None:
                return previous

        mangakakalot = Mangakakalot()
        manga = mangakakalot.get_manga_info(args['url'])

        model = MangaModel.from_manga(manga)

        access = MangaAccess(manga.title)
        previous = access.get_info()
        if previous is not None:
            model.persist(previous)

        model = manga_linked(vars(model))
        access.set_info(model)
        return model
