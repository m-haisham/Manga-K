from flask_api import status
from flask_restful import Resource

from database.access import MangaAccess
from rest.error import error_message


class Page(Resource):
    def get(self, manga_slug, chapter_slug, i):

        access = MangaAccess.map(manga_slug)
        chapter_info = access.get_chapter_by_slug(chapter_slug)

        if chapter_info.downloaded:
            page = chapter_info['pages'][i]
            del page['path']

        else:
            return error_message(f'{chapter_slug} not downloaded / missing'), status.HTTP_404_NOT_FOUND
