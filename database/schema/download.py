import marshmallow


class DownloadSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'manga_id', 'chapter_id', 'value', 'max')


download_schema = DownloadSchema()
downloads_schema = DownloadSchema(many=True)
