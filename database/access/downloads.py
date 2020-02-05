import shutil

from pathlib import Path
from threading import Lock

from tinydb import Query
from tinyrecord import transaction

from background.models import DownloadModel
from rest.encoding import page_link
from . import MangaAccess
from .. import mainbase, mangabase

from background import BackgroundDownload

from typing import List

from ..models import ChapterModel

dbmodel = Query()


class DownloadAccess:
    maindb = mainbase.get()
    mangadb = mangabase.get()
    dthread = BackgroundDownload.get()

    mutex = Lock()
    downloads = []

    def add(self, model):
        """
        Add download to queue
        Update thumbnail_path and link of pages of chapter

        :param model: model to download
        :return: true if added else false
        """
        access = MangaAccess(model.manga_title)

        # already in progress
        if any([download.url == model.url for download in self.downloads]):
            return False

        # already downloaded
        if access.get_chapter_by_url(model.url)['downloaded']:
            return False

        with transaction(self.maindb.downloads):
            self.maindb.downloads.upsert(model.todict(), dbmodel.url == model.url)

        self.dthread.queue.put(model)
        self.downloads.append(model)

        for i, page in enumerate(model.pages):
            page.thumbnail_path = str(model.thumbnail_path / Path(f'{i + 1}.jpg'))
            page.link = page_link(model.manga_title, model.title, i+1)

        access.update_pages([model.todict()])
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

    def remove(self, url):
        """
        Remove matching url from downloads database table

        :param url: url to be removed
        :return: None
        """
        with transaction(self.maindb.downloads):
            self.maindb.downloads.remove(dbmodel.url == url)
            for i, download in enumerate(self.downloads):
                if download.url == url:
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
                    page['thumbnail_path'] = ''
                    page['link'] = ''

                shutil.rmtree(info['thumbnail_path'])

                chapter_model = ChapterModel.fromdict(info)
                access.update_chapters_downloaded([chapter_model])
                access.update_pages([info])

    @staticmethod
    def load_from_database():
        """
        load from database and add to queue

        :return:
        """
        with transaction(DownloadAccess.maindb.downloads):
            models = [DownloadModel.fromdict(model) for model in DownloadAccess.maindb.downloads.all()]
            access = DownloadAccess()

            for model in models:
                access.add(model)
