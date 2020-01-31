import asyncio

from flask_api import status
from flask_restful import Resource, reqparse

from database.models import ChapterModel, PageModel
from database.access import DownloadAccess, MangaAccess

from background.models import DownloadModel
from network.scrapers import Mangakakalot
from rest.error import error_message

download_access = DownloadAccess()

parser = reqparse.RequestParser()
parser.add_argument('manga_url', required=True)
parser.add_argument('urls', action='append', required=True)


class DownloadsList(Resource):
    def get(self):
        downloads = download_access.get_all()

        models = []
        for model in downloads:
            d_model = model.todict()

            del d_model['path']
            del d_model['pages']

            models.append(d_model)

        return models

    def post(self):  # add download
        args = parser.parse_args()

        mangakakalot = Mangakakalot()

        manga_access = MangaAccess.map(args['manga_url'])
        if manga_access is None:
            return error_message('Manga not found in database', url=args['manga_url']), status.HTTP_404_NOT_FOUND

        info = manga_access.get_info()

        models = []
        for url in args['urls']:
            d_chapter = manga_access.get_chapter_by_url(url)

            pages = [PageModel.from_page(page) for page in mangakakalot.get_page_list(ChapterModel.fromdict(d_chapter))]
            model = DownloadModel.create(info, d_chapter, pages)
            response = download_access.add(model)

            d_model = model.todict()
            del d_model['path']
            del d_model['pages']

            # no progress checks if download adding failed
            if not response:
                del d_model['value']
                del d_model['max']

            models.append(d_model)

        return models


class Download(Resource):
    def get(self, i):
        download = download_access.get(i)
        if download is None:
            return error_message('Model of index does not exist', length=len(download_access.get_all())), \
                   status.HTTP_404_NOT_FOUND

        d_model = download.todict()
        del d_model['path']
        del d_model['pages']

        return d_model


class DownloadStatus(Resource):
    status_parser = reqparse.RequestParser()
    status_parser.add_argument('pause', type=bool)
    status_parser.add_argument('clear', type=bool)

    def get(self):
        return download_access.get_status()

    def post(self):
        args = self.status_parser.parse_args()

        return download_access.set_status(args['pause'], args['clear'])


class DownloadDelete(Resource):
    def post(self):
        args = parser.parse_args()

        manga_access = MangaAccess.map(args['manga_url'])
        if manga_access is None:
            return error_message('Manga not found in database', url=args['manga_url']), status.HTTP_404_NOT_FOUND

        # async operation, as deleting folders can take time
        asyncio.run(download_access.delete(manga_access, args['urls']))

        # prepare output
        chapters = []
        for url in args['urls']:
            chapter_model = manga_access.get_chapter_by_url(url)
            chapter_model['downloaded'] = False
            del chapter_model['pages']

            chapters.append(chapter_model)

        return chapters
