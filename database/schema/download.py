import marshmallow


class DownloadSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'manga_id', 'chapter_id', 'value', 'max')


class NoDownloadSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'manga_id', 'chapter_id')


download_schema = DownloadSchema()
nodownload_schema = NoDownloadSchema()
downloads_schema = DownloadSchema(many=True)
