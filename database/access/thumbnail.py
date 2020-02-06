from pathlib import Path

import requests

from database import LocalSession
from database.models.thumbnail import Thumbnail


class ThumbnailAccess:

    @staticmethod
    def upsert(thumbnail, commit=True):
        old = LocalSession.session.query(Thumbnail).filter_by(manga_id=thumbnail.manga_id).first()
        if old is None:
            LocalSession.session.add(thumbnail)
        else:
            old.url = thumbnail.url

        if commit:
            LocalSession.session.commit()

    @staticmethod
    def update(thumbnail, **kwargs):
        for key, value in kwargs.items():
            if key in ['id']:
                continue

            if hasattr(thumbnail, key) and value is not None:
                setattr(thumbnail, key, value)

        LocalSession.session.commit()

    @staticmethod
    def save(url, path):
        """
        Download and save the thumbnail url to self.thumbnail_path

        :return: None
        """
        #: create parent directory
        path.parent.mkdir(parents=True, exist_ok=True)

        response = requests.get(url=url)
        with path.open('wb') as thumbnail:
            thumbnail.write(response.content)

    @staticmethod
    def byte_stream(path):
        """
        :return: byte data from thumbnail file if it exists else :returns: None
        """
        if path.exists() and path.is_file():
            with path.open('rb') as thumbnail:
                data = thumbnail.read()

            return data
        else:
            raise FileNotFoundError('Thumbnail not downloaded')

    @staticmethod
    def exists(path):
        return path.exists() and path.is_file()