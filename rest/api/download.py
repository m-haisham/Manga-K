import asyncio

from flask_restful import Resource, reqparse

from background import BackgroundDownload
from database import LocalSession
from database.access import DownloadAccess, MangaAccess
from database.models import DownloadModel, ChapterModel, PageModel
from database.schema import download_schema, downloads_schema, nodownload_schema, chapters_schema
from network.scrapers import Mangakakalot

download_access = DownloadAccess()


class DownloadsList(Resource):
    download_parser = reqparse.RequestParser()
    download_parser.add_argument('manga_id', required=True)
    download_parser.add_argument('chapter_ids', action='append', required=True)

    def get(self):
        return DownloadAccess.downloads

    def post(self):  # add download
        args = self.download_parser.parse_args()

        BackgroundDownload.paused.value = True

        additions = []

        manga_access = MangaAccess(args['manga_id'])
        for chapter_id in args['chapter_ids']:
            chapter = LocalSession.session.query(ChapterModel).get(chapter_id)
            if chapter is None:
                continue

            # get pages
            mangakakalot = Mangakakalot()
            pages = mangakakalot.get_page_list(chapter)

            page_models = [PageModel(page.url, chapter_id) for page in pages]

            for page_model in page_models:
                old = LocalSession.session.query(PageModel).filter_by(url=page_model.url).first()
                if old is None:
                    LocalSession.session.add(page_model)

            model = DownloadModel.create(manga_access.id, chapter_id)
            response = download_access.add(model)

            LocalSession.session.flush()
            if response:
                additions.append(download_schema.dump(model))
            else:
                download_id = None
                for download in DownloadAccess.downloads:
                    if download['chapter_id'] == model.chapter_id:
                        download_id = download['id']

                model.id = download_id
                additions.append(nodownload_schema.dump(model))

        LocalSession.session.commit()
        BackgroundDownload.paused.value = False
        return additions


class Download(Resource):
    def get(self, i):
        # return DownloadAccess.downloads[i - 1]
        return downloads_schema.dump(LocalSession.session.query(DownloadModel).all())


class DownloadStatus(Resource):
    status_parser = reqparse.RequestParser()
    status_parser.add_argument('paused', type=bool)
    status_parser.add_argument('clear', type=bool)

    def get(self):
        return {
            "paused": BackgroundDownload.paused.value
        }

    def post(self):
        args = self.status_parser.parse_args()

        if args['paused'] is not None:
            BackgroundDownload.paused.value = args['paused']

        if args['clear'] is not None:
            BackgroundDownload.clear.value = args['clear']

        return {
            "paused": BackgroundDownload.paused.value
        }


class DownloadDelete(Resource):
    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument('ids', action='append', required=True)

    def post(self):
        args = self.delete_parser.parse_args()

        chapters = LocalSession.session.query(ChapterModel).filter(ChapterModel.id.in_(args['ids'])).all()

        asyncio.run(download_access.delete([chapter.path for chapter in chapters]))

        for chapter in chapters:
            chapter.downloaded = False

        LocalSession.session.commit()

        return chapters_schema.dump(chapters)