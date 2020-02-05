from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('manga_url', required=True)
parser.add_argument('urls', action='append', required=True)


class DownloadsList(Resource):
    def get(self):
        pass

    def post(self):  # add download
        pass


class Download(Resource):
    def get(self, i):
        pass


class DownloadStatus(Resource):
    status_parser = reqparse.RequestParser()
    status_parser.add_argument('pause', type=bool)
    status_parser.add_argument('clear', type=bool)

    def get(self):
        pass

    def post(self):
        pass


class DownloadDelete(Resource):
    def post(self):
        pass
