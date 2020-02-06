import marshmallow


class UndownloadedSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'url',)


class DownloadedSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'url', 'link')


pages_downloaded_schema = DownloadedSchema(many=True)
pages_schema = UndownloadedSchema(many=True)
