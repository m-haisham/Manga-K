from flask_restful import Resource, reqparse

from database import LocalSession
from database.access import MangaAccess, RecentsAccess
from database.models import PageModel, RecentModel
from database.schema import chapter_schema, pages_schema, pages_downloaded_schema
from network import NetworkHelper
from network.scrapers import Mangakakalot


class Chapter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('read', type=bool)

    def get(self, manga_id, chapter_id):

        # get information
        access = MangaAccess(manga_id)
        manga_model = access.get_or_404()

        chapter_model = access.chapter_or_404(chapter_id)

        chapter_info = chapter_schema.dump(chapter_model)
        chapter_model.read = True

        # add to recents
        recent = RecentModel.create(manga_id, chapter_id)
        RecentsAccess.upsert(recent, commit=False)

        # arrange information
        if chapter_model.downloaded:  # give link to pages if downloaded
            chapter_info['pages'] = pages_downloaded_schema.dump(chapter_model.pages)

        elif NetworkHelper.is_connected():
            mangakakalot = Mangakakalot()
            pages = mangakakalot.get_page_list(chapter_model)

            page_models = [PageModel(page.url, chapter_id) for page in pages]

            for page_model in page_models:
                old = LocalSession.session.query(PageModel).filter_by(url=page_model.url).first()
                if old is None:
                    LocalSession.session.add(page_model)

            chapter_info['pages'] = pages_schema.dump(page_models)
        else:
            chapter_info['pages'] = pages_schema.dump(chapter_model.pages)

        LocalSession.session.commit()
        return chapter_info

    def post(self, manga_id, chapter_id):
        args = self.parser.parse_args()

        # get information
        access = MangaAccess(manga_id)
        chapter_model = access.chapter_or_404(chapter_id)

        chapter_model.read = args['read']
        LocalSession.session.commit()

        return chapter_schema.dump(chapter_model)
