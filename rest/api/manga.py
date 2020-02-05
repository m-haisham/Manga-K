from flask import jsonify
from flask_api import status
from flask_restful import Resource, reqparse

from database.Schema import mangas_schema, manga_schema
from database.access import MangaAccess
from database.models import MangaModel, ChapterModel
from network import NetworkHelper
from network.scrapers import Mangakakalot
from store import chapter_path, sanitize
from ..encoding import chapter_link
from ..error import error_message

pref_parser = reqparse.RequestParser()
pref_parser.add_argument('manhwa', type=bool)
pref_parser.add_argument('favourite', type=bool)


class Manga(Resource):
    def get(self, manga_slug):
        access = MangaAccess.map(manga_slug)
        if access is None:
            return error_message(f'{manga_slug} does not exist', condition='manga'), \
                   status.HTTP_404_NOT_FOUND

        info = access.get_info()
        if info is None:
            access.purge()
            return error_message(f'{manga_slug} not found'), status.HTTP_404_NOT_FOUND

        info['updates'] = []
        # update chapters
        if NetworkHelper.is_connected():
            mangakakalot = Mangakakalot()

            # TODO update info and thumbnail

            chapters = mangakakalot.get_chapter_list(info['url'])
            models = [
                ChapterModel.from_chapter(
                    chapter,
                    link=chapter_link(info['title'], chapter.title),
                    path=str(chapter_path(info['title'], chapter.title))
                ) for chapter in chapters
            ]

            saved_urls = [chapter['url'] for chapter in access.get_chapters()]

            updates = []
            for chapter in models:
                if chapter.url in saved_urls:
                    saved_urls.remove(chapter.url)
                else:
                    updates.append(chapter)

            access.update_chapters(updates)

            info['updates'] = [sanitize(chapter.todict()) for chapter in updates]

        info['chapters'] = [sanitize(chapter) for chapter in access.get_chapters()]
        return info

    def post(self, manga_slug):
        args = pref_parser.parse_args()

        access = MangaAccess.map(manga_slug)

        manga = access.get_info()
        if manga is None:
            access.purge()
            return error_message(f'{manga_slug} not found'), status.HTTP_404_NOT_FOUND

        for key, value in args.items():
            if value is not None:
                manga[key] = value

        access.set_info(manga)

        return manga


url_parser = reqparse.RequestParser()
url_parser.add_argument('url', type=str)


class MangaList(Resource):
    def get(self):
        result = mangas_schema.dump(MangaAccess.all())
        return jsonify(result)

    def post(self):
        args = url_parser.parse_args()

        connected = NetworkHelper.is_connected()

        model = MangaAccess.map(args['url'])
        if model is not None:

            if not connected:
                return manga_schema.dump(model)

        mangakakalot = Mangakakalot()
        manga = mangakakalot.get_manga_info(args['url'])

        manga_model = MangaModel.from_manga(manga)

        access, inserted = MangaAccess.gesert(manga_model)

        if not inserted:
            # update and persist
            manga_model = access.update(**vars(manga))

        # insert chapters
        chapters = mangakakalot.get_chapter_list(manga.url)
        models = [
            ChapterModel.from_chapter(
                chapter,
                manga_id=manga_model.id,
                path=str(chapter_path(manga.title, chapter.title))
            ) for chapter in chapters
        ]

        access.insert_chapters(models)

        # # set thumbnail
        # ThumbnailAccess(model['title'], model['thumbnail_url'])

        result = manga_schema.dump(manga_model)
        return result
