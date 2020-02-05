import io

from flask import send_file
from flask_api import status
from flask_restful import Resource, reqparse, abort

from database.access import ThumbnailAccess, MangaAccess
from rest.error import error_message


class Thumbnail(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', help='thumbnail url', required=True)

    def get(self, manga_id):

        model = MangaAccess(manga_id).get_or_404()
        thumbnail = model.thumbnail[0]

        if thumbnail is None:
            abort(status.HTTP_404_NOT_FOUND)

        if thumbnail.url != model.thumbnail_url or not ThumbnailAccess.exists(thumbnail.path):
            ThumbnailAccess.save(model.thumbnail_url, thumbnail.path)

        return send_file(
            io.BytesIO(ThumbnailAccess.byte_stream(thumbnail.path)),
            as_attachment=True,
            attachment_filename='thumbnail.jpg',
            mimetype='image/jpeg'
        )

    def post(self, manga_id):
        args = self.parser.parse_args()

        model = MangaAccess(manga_id).get_or_404()
        thumbnail = model.thumbnail[0]

        ThumbnailAccess.update(thumbnail, url=args['url'])
