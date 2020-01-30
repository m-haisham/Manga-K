from pathlib import Path
from threading import Lock

from tinydb import Query

from background.models import DownloadModel
from rest.encoding import page_link
from . import MangaAccess
from .. import mainbase, mangabase

from background import BackgroundDownload

dbmodel = Query()


class DownloadAccess:
    maindb = mainbase.get()
    mangadb = mangabase.get()
    dthread = BackgroundDownload.get()

    mutex = Lock()
    downloads = []

    def add(self, model):
        """
        add download to queue

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

        self.maindb.downloads.upsert(model.todict(), dbmodel.url == model.url)

        self.dthread.queue.put(model)
        self.downloads.append(model)

        for i, page in enumerate(model.pages):
            page.path = str(model.path / Path(f'{i + 1}.jpg'))
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

    @staticmethod
    def load_from_database():
        """
        laod from database and add to queue

        :return:
        """
        models = [DownloadModel.fromdict(model) for model in DownloadAccess.maindb.downloads.all()]
        access = DownloadAccess()

        for model in models:
            access.add(model)
