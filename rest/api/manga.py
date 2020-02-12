from flask import jsonify
from flask_restful import Resource, reqparse

from database.access import MangaAccess, ThumbnailAccess
from database.models import MangaModel, ChapterModel
from database.models.thumbnail import Thumbnail
from database.schema import mangas_schema, manga_schema, chapters_schema, recent_schema
from network import NetworkHelper
from network.scrapers import Mangakakalot
from store import chapter_path

pref_parser = reqparse.RequestParser()
pref_parser.add_argument('manhwa', type=bool)
pref_parser.add_argument('favourite', type=bool)


class Manga(Resource):
    def get(self, manga_id):
        access = MangaAccess(manga_id)

        model = access.get_or_404()
        info = manga_schema.dump(model)

        # update chapters
        if NetworkHelper.is_connected():
            mangakakalot = Mangakakalot()

            manga = mangakakalot.get_manga_info(model.url)
            manga_model = access.update(**vars(manga))

            info = manga_schema.dump(manga_model)

            # set thumbnail
            thumbnail = Thumbnail(manga_model)
            ThumbnailAccess.upsert(thumbnail)

            saved_urls = [chapter.url for chapter in access.get_chapters()]
            parsed = mangakakalot.get_chapter_list(model.url)

            updates = []
            for chapter in parsed:
                if chapter.url in saved_urls:
                    saved_urls.remove(chapter.url)
                else:
                    updates.append(ChapterModel.from_chapter(
                        chapter,
                        manga_id=model.id,
                        path=chapter_path(model.title, chapter.title)
                    ))

            access.insert_chapters(updates)
            info['updates'] = chapters_schema.dump(updates)
        else:
            info['updates'] = []

        info['recent'] = recent_schema.dump(model.recent)
        info['chapters'] = chapters_schema.dump(access.get_chapters())
        return info

    def post(self, manga_id):
        args = pref_parser.parse_args()

        access = MangaAccess(manga_id)

        # Check if manga exists
        access.get_or_404()

        model = access.update(**args)

        return manga_schema.dump(model)


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
                path=chapter_path(manga.title, chapter.title)
            ) for chapter in chapters
        ]

        access.insert_chapters(models)

        # set thumbnail
        thumbnail = Thumbnail(manga_model)
        ThumbnailAccess.upsert(thumbnail)

        result = manga_schema.dump(manga_model)
        return result
