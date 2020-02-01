from flask_api import status
from flask_restful import Resource

from database.access import MangaAccess
from database.models import ChapterModel
from network.scrapers import Mangakakalot
from rest.encoding import chapter_link
from rest.error import error_message
from store import chapter_path


class Updates(Resource):
    def get(self, manga_slug):

        # get information
        access = MangaAccess.map(manga_slug)
        if access is None:
            return error_message(f'{manga_slug} does not exist', condition='manga'), \
                   status.HTTP_412_PRECONDITION_FAILED

        mangakakalot = Mangakakalot()
        manga_info = access.get_info()

        # arrange
        saved_urls = [chapter['url'] for chapter in access.get_chapters()]
        parsed = [
            ChapterModel.from_chapter(
                chapter,
                link=chapter_link(manga_info['title'], chapter.title),
                path=str(chapter_path(manga_info['title'], chapter.title))
            ).todict() for chapter in mangakakalot.get_chapter_list(manga_info['url'])
        ]

        updates = []
        for chapter in parsed:
            if chapter['url'] in saved_urls:
                saved_urls.remove(chapter['url'])
            else:
                updates.append(chapter)

        for chapter in updates:
            del chapter['path']

        return updates
