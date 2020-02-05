from pathlib import Path

import requests


class ThumbnailAccess:

    def __init__(self, title, url):
        """
        :param title: title of manga (Normal/Slugged)
        :param url: url of thumbnail
        """
        self.url = url
        self.path = Path('.')
        pass

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
        pass
