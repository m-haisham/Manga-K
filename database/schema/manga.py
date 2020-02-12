import marshmallow


class MangaSchema(marshmallow.Schema):
    class Meta:
        fields = (
            'id', 'title', 'status', 'description', 'genres', 'url', 'thumbnail_url', 'manhwa', 'favourite', 'added', 'style')

class DiscoverSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'title', 'url', 'thumbnail_url', 'manhwa', 'favourite', 'added')

manga_schema = MangaSchema()
mangas_schema = MangaSchema(many=True)

discover_schema = DiscoverSchema(many=True)