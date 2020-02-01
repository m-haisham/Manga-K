import io

from flask import send_file
from flask_api import status
from flask_restful import Resource, reqparse

from database.access import ThumbnailAccess
from rest.error import error_message


class Thumbnail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', help='thumbnail url', required=True)

    def get(self, manga_slug):

        thumbnail = ThumbnailAccess.data(manga_slug)
        if thumbnail is None:
            return error_message('Not Found'), status.HTTP_404_NOT_FOUND

        if not thumbnail.downloaded:
            thumbnail.save()

        return send_file(
            io.BytesIO(thumbnail.byte_stream()),
            as_attachment=True,
            attachment_filename='thumbnail.jpg',
            mimetype='image/jpeg'
        )

    def post(self, manga_slug):
        args = self.parser.parse_args()

        ThumbnailAccess(manga_slug, args['url'])