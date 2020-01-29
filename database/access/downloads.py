from threading import Lock

from tinydb import Query

from background.models import DownloadModel
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
        if any([download.url == model.url for download in self.downloads]):
            return False

        self.maindb.downloads.upsert(model.todict(), dbmodel.url == model.url)

        self.dthread.queue.put(model)
        self.downloads.append(model)
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
