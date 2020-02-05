from flask_api import status
from flask_restful import Resource

from database.Schema import manga_schema, chapters_schema
from database.access import MangaAccess
from database.models import ChapterModel
from network.scrapers import Mangakakalot
from rest.encoding import chapter_link
from rest.error import error_message
from store import chapter_path


class Updates(Resource):
    def get(self, manga_id):

        # get information
        access = MangaAccess(manga_id)

        model = access.get_or_404()

        mangakakalot = Mangakakalot()

        # arrange
        saved_urls = [chapter.url for chapter in access.get_chapters()]
        parsed = mangakakalot.get_chapter_list(model.url)

        updates = []
        for chapter in parsed:
            if chapter.url in saved_urls:
                saved_urls.remove(chapter.url)
            else:
                updates.append(ChapterModel.from_chapter(
                    chapter,
                    manga_id=model.id,
                    path=chapter_path(model.title, chapter.title)
                ))

        return chapters_schema.dump(updates)
