from flask_api import status
from flask_restful import Resource, reqparse

from database.access import MangaAccess, RecentsAccess
from database.models import MangaModel, ChapterModel, PageModel, RecentModel
from network import NetworkHelper
from network.scrapers import Mangakakalot
from ..error import error_message


class Chapter(Resource):

    def get(self, manga_slug, chapter_slug):

        # get information
        access = MangaAccess.map(manga_slug)
        if access is None:
            return error_message(f'{manga_slug} does not exist', condition='manga'), \
                   status.HTTP_412_PRECONDITION_FAILED

        chapter_info = access.get_chapter_by_slug(chapter_slug)
        if chapter_info is None:
            return error_message(f'/{manga_slug}/{chapter_slug} not found', condition='chapter'), \
                   status.HTTP_412_PRECONDITION_FAILED

        manga_info = access.get_info()
        chapter_info['manga'] = manga_info['link']
        models = chapter_info['pages']

        # add to recents
        recent_model = RecentModel.create(ChapterModel.fromdict(chapter_info), manga_info['title'], manga_info['link'])
        RecentsAccess().add(recent_model)

        # arrange information
        if chapter_info['downloaded']:  # give link to pages if downloaded
            chapter_info['pages'] = [PageModel.from_dict(page).clean_dict() for page in models]

        elif NetworkHelper.is_connected():
            mangakakalot = Mangakakalot()
            pages = mangakakalot.get_page_list(ChapterModel.fromdict(chapter_info))

            # if downloaded pages are already loaded
            if not chapter_info['downloaded']:
                models = [PageModel.from_page(page).to_dict() for page in pages]
                chapter_info['pages'] = models

                access.update_pages([chapter_info])

            chapter_info['pages'] = [vars(page) for page in pages]

        del chapter_info['path']

        return chapter_info
