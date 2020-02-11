import io
from pathlib import Path

from flask import send_file
from flask_api import status
from flask_restful import Resource

from database import LocalSession
from database.access import MangaAccess, RecentsAccess
from database.models import PageModel, RecentModel
from database.schema import pages_schema, pages_downloaded_schema
from network import NetworkHelper
from network.scrapers import Mangakakalot
from rest.error import error_message


class PageList(Resource):
    def get(self, manga_id, chapter_id):

        # get information
        access = MangaAccess(manga_id)
        manga_model = access.get_or_404()

        chapter_model = access.chapter_or_404(chapter_id)
        chapter_model.read = True

        # add to recents
        recent = RecentModel.create(manga_id, chapter_id)
        RecentsAccess.upsert(recent, commit=False)

        # arrange information
        if chapter_model.downloaded:  # give link to pages if downloaded
            pages = pages_downloaded_schema.dump(chapter_model.pages)

        elif NetworkHelper.is_connected():
            mangakakalot = Mangakakalot()
            pages = mangakakalot.get_page_list(chapter_model)

            page_models = [PageModel(page.url, chapter_id) for page in pages]

            for page_model in page_models:
                old = LocalSession.session.query(PageModel).filter_by(url=page_model.url).first()
                if old is None:
                    LocalSession.session.add(page_model)

            pages = pages_schema.dump(page_models)
        else:
            pages = pages_schema.dump(chapter_model.pages)

        LocalSession.session.commit()

        return pages


class Page(Resource):
    def get(self, manga_id, chapter_id, i):

        # adjusting index
        i -= 1

        access = MangaAccess(manga_id)
        chapter_model = access.chapter_or_404(chapter_id)

        if chapter_model.downloaded:
            if i < 0 or i >= len(chapter_model.pages):
                return error_message(
                    f'page number must be greater than 0 and less than or equal to {len(chapter_info["pages"])}',
                    length=len(chapter_model.pages)
                ), status.HTTP_400_BAD_REQUEST

            page = chapter_model.pages[i]

            with Path(page.path).open('rb') as fb:
                stream = fb.read()

            return send_file(
                io.BytesIO(stream),
                mimetype='image/jpeg',
                as_attachment=True,
                attachment_filename=f'{i + 1}.jpg'
            )
        else:
            return error_message('Chapter not downloaded', condition='download'), \
                   status.HTTP_404_NOT_FOUND
