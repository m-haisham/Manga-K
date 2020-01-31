import io
from pathlib import Path

from flask import send_file
from flask_api import status
from flask_restful import Resource

from database.access import MangaAccess
from database.models import PageModel, ChapterModel
from network import NetworkHelper
from network.scrapers import Mangakakalot
from rest.error import error_message


class PageList(Resource):
    def get(self, manga_slug, chapter_slug):
        access = MangaAccess.map(manga_slug)
        if access is None:
            return error_message(f'{manga_slug} does not exist', condition='manga'),\
                   status.HTTP_412_PRECONDITION_FAILED

        chapter_info = access.get_chapter_by_slug(chapter_slug)
        if chapter_info is None:
            return error_message(f'{chapter_slug} does not exist', condition='chapter'),\
                   status.HTTP_412_PRECONDITION_FAILED

        pages = []
        models = chapter_info['pages']

        # give link to pages if downloaded
        if chapter_info['downloaded']:
            pages = [PageModel.from_dict(page).clean_dict() for page in models]

        elif NetworkHelper.is_connected():
            mangakakalot = Mangakakalot()
            pages = mangakakalot.get_page_list(ChapterModel.fromdict(chapter_info))

            if not chapter_info['downloaded']:
                models = [PageModel.from_page(page).to_dict() for page in pages]
                chapter_info['pages'] = models

                access.update_pages([chapter_info])

            pages = [vars(page) for page in pages]

        return pages


class Page(Resource):
    def get(self, manga_slug, chapter_slug, i):

        # adjusting index
        i -= 1

        access = MangaAccess.map(manga_slug)
        if access is None:
            return error_message(f'{manga_slug} does not exist', condition='manga'),\
                   status.HTTP_412_PRECONDITION_FAILED

        chapter_info = access.get_chapter_by_slug(chapter_slug)
        if chapter_info is None:
            return error_message(f'{chapter_slug} does not exist', condition='chapter'),\
                   status.HTTP_412_PRECONDITION_FAILED

        if chapter_info['downloaded']:
            if i < 0 or i >= len(chapter_info['pages']):
                return error_message(
                    f'page number must be greater than 0 and less than or equal to {len(chapter_info["pages"])}',
                    length=len(chapter_info['pages'])
                ), status.HTTP_400_BAD_REQUEST

            page = chapter_info['pages'][i]

            with Path(page['path']).open('rb') as fb:
                stream = fb.read()

            return send_file(
                io.BytesIO(stream),
                mimetype='image/jpeg',
                as_attachment=True,
                attachment_filename=f'{i+1}.jpg'
            )
        else:
            return error_message('Chapter not downloaded', condition='download'),\
                   status.HTTP_412_PRECONDITION_FAILED
