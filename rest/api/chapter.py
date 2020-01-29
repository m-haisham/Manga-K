from flask_api import status
from flask_restful import Resource, reqparse

from database.access import MangaAccess
from database.models import MangaModel, ChapterModel
from network import NetworkHelper
from network.scrapers import Mangakakalot
from ..encoding import UrlEncoding


class Chapter(Resource):
    def get(self, manga_title, chapter_title):

        manga_title = UrlEncoding.back(manga_title)
        chapter_title = UrlEncoding.back(chapter_title)

        access = MangaAccess(manga_title)

        info = access.get_chapter_by_title(chapter_title)
        if info is None:
            return dict(message=f'{manga_title}/{chapter_title} not found'), status.HTTP_404_NOT_FOUND

        info['manga'] = access.get_info()['link']

        pages = []
        if NetworkHelper.is_connected():

            mangakakalot = Mangakakalot()
            pages = mangakakalot.get_page_list(ChapterModel.fromdict(info))

        info['pages'] = [vars(page) for page in pages]

        return info
