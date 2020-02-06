from flask_restful import Resource, reqparse

from background import BackgroundDownload
from database.access import DownloadAccess
from database.schema import download_schema, downloads_schema


class DownloadsList(Resource):
    download_parser = reqparse.RequestParser()
    download_parser.add_argument('manga_url', required=True)
    download_parser.add_argument('urls', action='append', required=True)

    def get(self):
        return DownloadAccess.downloads

    def post(self):  # add download
        args = self.download_parser.parse_args()


class Download(Resource):
    def get(self, i):
        return DownloadAccess.downloads[i - 1]


class DownloadStatus(Resource):
    status_parser = reqparse.RequestParser()
    status_parser.add_argument('paused', type=bool)
    status_parser.add_argument('clear', type=bool)

    def get(self):
        return {
            "paused": BackgroundDownload.paused.value
        }

    def post(self):
        args = self.status_parser.parse_args()

        if args['paused'] is not None:
            BackgroundDownload.paused.value = args['paused']

        if args['clear'] is not None:
            BackgroundDownload.paused.value = args['clear']

        return {
            "paused": BackgroundDownload.paused.value
        }


class DownloadDelete(Resource):
    def post(self):
        pass
