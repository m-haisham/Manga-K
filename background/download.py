from threading import Thread
from queue import Queue

from .chapter import ChapterDownload


class BackgroundDownload(Thread):
    _instance = None

    def __init__(self):
        super(BackgroundDownload, self).__init__(daemon=True)

        self.queue = Queue()

    def run(self) -> None:

        from database.access import DownloadAccess, MangaAccess

        d_access = DownloadAccess()

        # download loop
        while True:
            model = self.queue.get()
            m_access = MangaAccess(model.manga_title)

            print(f'Downloading {model.url}')
            ChapterDownload(model).start()

            model.downloaded = True
            d_access.remove(model.url)
            m_access.update_chapters_downloaded([model])
            print(f'Download Complete {model.url}')

    @staticmethod
    def get():
        if BackgroundDownload._instance is None:
            # instantiate and start thread
            BackgroundDownload._instance = BackgroundDownload()
            BackgroundDownload._instance.start()

        return BackgroundDownload._instance
