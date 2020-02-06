from queue import Queue
from threading import Thread

from database import LocalSession
from database.models import ChapterModel, DownloadModel
from .chapter import ChapterDownload
from .models import AtomicBoolean


class BackgroundDownload(Thread):
    _instance = None
    session = None

    paused = AtomicBoolean(False)
    clear = AtomicBoolean(False)

    def __init__(self):
        super(BackgroundDownload, self).__init__(daemon=True)

        self.queue = Queue()

    def run(self) -> None:

        from database.access import DownloadAccess

        download_access = DownloadAccess()

        # download loop
        while True:
            model = self.queue.get()

            while self.paused.value:
                pass

            with LocalSession.instance as session:
                ch = session.query(ChapterModel).get(model['chapter_id'])
                pg = ch.pages

            ChapterDownload(model, ch, pg, self.paused, self.clear).start()

            download_access.remove(model['chapter_id'])
            if self.clear.value:
                # clear the queue
                while not self.queue.empty():
                    model = self.queue.get()
                    download_access.remove(model['chapter_id'])

                # reset
                self.clear.value = False
                continue

            # update database
            with LocalSession.instance as session:
                chapter = session.query(ChapterModel).get(model['chapter_id'])
                chapter.downloaded = True

                download = session.query(DownloadModel).filter_by(chapter_id=model['chapter_id']).first()
                session.delete(download)
                session.commit()

    @staticmethod
    def get():
        if BackgroundDownload._instance is None:
            # instantiate and start thread
            BackgroundDownload._instance = BackgroundDownload()
            BackgroundDownload._instance.start()

        return BackgroundDownload._instance
