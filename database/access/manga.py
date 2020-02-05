from flask import abort
from flask_api import status
from typing import Union, List

from database import LocalSession
from database.models import MangaModel, MangaMap, ChapterMap, ChapterModel


class MangaAccess:
    """
    Provides access to manga specific operations
    Only accesses manga database, its map and the specific table for the manga

    Manga title is used as key for the table
    Map is used to get the title of manga or url of chapter.
    """

    def __init__(self, id: int):
        """
        :param id: id of manga
        """
        self.id = id

    def get_or_404(self):
        model = LocalSession.session.query(MangaModel).get(self.id)
        if model is None:
            abort(status.HTTP_404_NOT_FOUND)

        return model

    def update_chapters(self, chapters):
        """
        if chapter exists Updates the chapters in database
        else adds the chapter to database and adds slog to map

        :param chapters: chapters to check against database
        :return: None
        """
        pass

    def update_pages(self, chapters):
        """
        Update pages of :param chapters:

        :return: None
        """
        pass

    def update_chapters_downloaded(self, chapters):
        """
        updates the downloaded get_status of the given chapters
        if chapter doesnt exist it is ignored

        :param chapters: chapters to update
        :return: None
        """
        pass

    def update_chapters_read(self, chapters):
        """
        updates the read status of the given chapters
        if chapter doesnt exist it is ignored

        :param chapters: chapters to update
        :return: None
        """
        pass

    def get_chapter_by_slug(self, slug) -> Union[dict, None]:
        """
        :return: return chapter which has matching title to :param title:
        """
        pass

    def get_chapter_by_url(self, url) -> Union[dict, None]:
        """
        :return: return chapter which has matching url to :param url:
        """
        pass

    def insert_chapters(self, models):
        """
        inserts the models if the model does not exist

        :param models: chapter models to insert
        :return: None
        """
        session = LocalSession.session

        for model in models:
            chapter_map = session.query(ChapterMap).filter_by(key=model.url).first()
            if chapter_map is None:  # insert
                session.add(model)
                session.flush()

                chapter_map = ChapterMap(model.url, model.id)
                session.add(chapter_map)
            else:
                model = session.query(ChapterModel).get(chapter_map.chapter_id)

        session.commit()

    def get_chapters(self) -> List[ChapterModel]:
        """
        :return: current stored chapters in the database
        """
        model = LocalSession.session.query(MangaModel).get(self.id)
        return model.chapters


    def update(self, **kwargs):
        model = LocalSession.session.query(MangaModel).get(self.id)

        for key, value in kwargs.items():
            if key in ['id', 'url']:
                continue

            if hasattr(model, key) and value is not None:
                setattr(model, key, value)

        LocalSession.session.commit()

        return model

    @staticmethod
    def gesert(model: MangaModel) -> tuple:
        """
        :param model: model to insert
        :return: access, inserted: bool
        """
        manga_map = MangaAccess.map(model.url)
        if manga_map is None:
            LocalSession.session.add(model)
            LocalSession.session.flush()

            mapping = MangaMap(model.url, model.id)
            LocalSession.session.add(mapping)

            LocalSession.session.commit()

            return MangaAccess(model.id), True
        else:
            return MangaAccess(manga_map.manga_id), False

    @staticmethod
    def exists(**kwargs) -> bool:
        """
        Return if doesnt exist insert new
        :param model: model to insert
        :return: model
        """
        model = LocalSession.session.query(MangaModel).filter_by(**kwargs).first()

        if model is None:
            return False
        else:
            return True

    @staticmethod
    def map(key) -> MangaMap:
        """
        :return: MangaAccess associated with :param key:
        """
        map = LocalSession.session.query(MangaMap).filter_by(key=key).first()

        return map

    @staticmethod
    def filter(**kwargs):
        return LocalSession.session.query(MangaModel).filter_by(**kwargs).all()

    @staticmethod
    def all():
        """
        :return: name of all manga tables in database
        """
        mangas = LocalSession.session.query(MangaModel).all()

        return mangas
