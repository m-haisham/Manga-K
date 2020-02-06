import shutil
from pathlib import Path
from threading import Lock
from typing import List

from tinydb import Query
from tinyrecord import transaction

from background import BackgroundDownload
from database.models import DownloadModel
from rest.encoding import page_link
from . import MangaAccess
from .. import LocalSession
from ..models import ChapterModel
from ..schema import download_schema

dbmodel = Query()


class DownloadAccess:
    dthread = BackgroundDownload.get()

    mutex = Lock()
    downloads = []

    def add(self, model):
        """
        Add download to queue
        Update path and link of pages of chapter

        :param model: model to download
        :return: true if added else false
        """
        chapter = LocalSession.session.query(ChapterModel).get(model.chapter_id)

        if chapter.manga_id != model.manga_id:
            return False

        # already in progress
        if any([download['chapter_id'] == model.chapter_id for download in self.downloads]):
            return False

        # already downloaded
        if chapter.downloaded:
            return False

        LocalSession.session.add(model)
        LocalSession.session.flush()

        model_dict = download_schema.dump(model)
        self.dthread.queue.put(model_dict)
        self.downloads.append(model_dict)

        for i, page in enumerate(chapter.pages):
            page.path = chapter.path / Path(f'{i + 1}.jpg')
            page.link = page_link(model.manga_id, model.chapter_id, i+1)

        LocalSession.session.commit()
        return True

    def get(self, i):
        """
        :return: download of index :param i:
        """
        try:
            return self.downloads[i]
        except IndexError:
            pass

    def get_all(self):
        """
        :return: all downloads
        """
        return self.downloads

    def remove(self, id):
        """
        Remove matching url from downloads database table

        :param url: url to be removed
        :return: None
        """
        for i, download in enumerate(self.downloads):
            if download['chapter_id'] == id:
                del self.downloads[i]
                break

    def remove_from_queue(self, i):
        """
        Remove index i from download queue

        :param i: index to be removed
        :return: None
        """
        pass

    def get_status(self):
        return dict(
            paused=self.dthread.paused.value,
            clear=self.dthread.clear.value
        )

    def set_status(self, paused=None, clear=None):
        """
        value is not set if arg is None

        :param paused: new value for paused
        :param clear: new value for clear
        :return: new value for reset flags
        """
        flags = {}
        if paused is not None:
            self.dthread.paused.value = paused
            flags['paused'] = paused

        if clear is not None:
            self.dthread.clear.value = clear
            flags['clear'] = clear

        return flags

    async def delete(self, access: MangaAccess, chapters: List[dict]):
        for chapter in chapters:
            info = access.get_chapter_by_url(chapter)

            if info['downloaded']:
                info['downloaded'] = False

                pages = info['pages']
                for page in pages:
                    page['path'] = ''
                    page['link'] = ''

                shutil.rmtree(info['path'])

                chapter_model = ChapterModel.fromdict(info)
                access.update_chapters_downloaded([chapter_model])
                access.update_pages([info])

    @staticmethod
    def load_from_database():
        """
        load from database and add to queue

        :return:
        """
        models = LocalSession.session.query(DownloadModel).all()
        access = DownloadAccess()

        for model in models:
            access.add(model)
