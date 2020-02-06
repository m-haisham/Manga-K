from flask_restful import Resource

from database.access import MangaAccess
from database.models import ChapterModel
from database.schema import chapters_schema
from network.scrapers import Mangakakalot
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
