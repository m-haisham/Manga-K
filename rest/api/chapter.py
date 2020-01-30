from flask_api import status
from flask_restful import Resource, reqparse

from database.access import MangaAccess
from database.models import MangaModel, ChapterModel, PageModel
from network import NetworkHelper
from network.scrapers import Mangakakalot
from ..encoding import UrlEncoding
from ..error import error_message


class Chapter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('delete', type=bool, default=False)

    def get(self, manga_title, chapter_title):

        args = self.parser.parse_args()

        manga_title = UrlEncoding.back(manga_title)
        chapter_title = UrlEncoding.back(chapter_title)

        access = MangaAccess(manga_title)

        chapter_info = access.get_chapter_by_title(chapter_title)
        if chapter_info is None:
            return error_message(f'/{manga_title}/{chapter_title} not found'), status.HTTP_404_NOT_FOUND

        chapter_info['manga'] = access.get_info()['link']

        pages = []
        models = chapter_info['pages']

        # give link to pages if downloaded
        if not args['delete'] and chapter_info['downloaded']:
            chapter_info['pages'] = [PageModel.from_dict(page).clean_dict() for page in models]

        elif NetworkHelper.is_connected():
            mangakakalot = Mangakakalot()
            pages = mangakakalot.get_page_list(ChapterModel.fromdict(chapter_info))

            # if downloaded pages are already loaded
            if not chapter_info['downloaded']:
                models = [PageModel.from_page(page) for page in pages]
                access.update_pages([chapter_info])

            chapter_info['pages'] = [vars(page) for page in pages]

        return chapter_info
