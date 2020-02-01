from pathlib import Path

from database import mainbase
from store import manga_path, slugify

import requests


class ThumbnailAccess:
    maindb = mainbase.get()
    thumbnails_table = mainbase.get().thumbnail.name

    def __init__(self, title, url):
        """
        :param title: title of manga (Normal/Slugged)
        :param url: url of thumbnail
        """
        self.title = slugify(title)
        self.path = manga_path(title) / Path('thumbnail.jpg')
        self.url = url

        #: Used to suggest whether the file exists or not
        self.downloaded = self.path.exists() and self.path.is_file()

        try:
            previous_url = self.maindb.get_key(self.title, self.thumbnails_table)
        except KeyError:  # no url saved
            pass
        else:
            if previous_url != self.url:  # url has changed
                if self.downloaded:  # file exists

                    #: remove file
                    self.path.unlink()
                    self.downloaded = False

        # save to database
        self.maindb.insert_key(self.title, self.url, self.thumbnails_table)

    def save(self):
        """
        Download and save the thumbnail url to self.path

        :return: None
        """

        #: create parent directory
        self.path.parent.mkdir(parents=True, exist_ok=True)

        response = requests.get(url=self.url)
        with self.path.open('wb') as thumbnail:
            thumbnail.write(response.content)

        self.downloaded = True

    def byte_stream(self):
        """
        :return: byte data from thumbnail file if it exists else :returns: None
        """
        if not self.downloaded:
            raise FileNotFoundError('Thumbnail not downloaded')

        with self.path.open('rb') as thumbnail:
            data = thumbnail.read()

        return data

    @staticmethod
    def data(title):
        """
        if title is not saved in database :returns: None

        :param title: title of manga (Normal/Slugged)
        :return: :class:`ThumbnailAccess` from database
        """
        try:
            url = ThumbnailAccess.maindb.get_key(slugify(title), ThumbnailAccess.thumbnails_table)
            return ThumbnailAccess(title, url)
        except KeyError:
            pass
