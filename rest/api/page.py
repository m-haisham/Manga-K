from flask_api import status
from flask_restful import Resource

from database.access import MangaAccess
from rest.encoding import UrlEncoding
from rest.error import error_message


class Page(Resource):
    def get(self, manga_title, chapter_title, i):

        manga_title = UrlEncoding.back(manga_title)
        chapter_title = UrlEncoding.back(chapter_title)

        access = MangaAccess(manga_title)
        chapter_info = access.get_chapter_by_title(chapter_title)

        if chapter_info.downloaded:
            page = chapter_info['pages'][i]
            del page['path']

        else:
            return error_message(f'{chapter_title} not downloaded / missing'), status.HTTP_404_NOT_FOUND
