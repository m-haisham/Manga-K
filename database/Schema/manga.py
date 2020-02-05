import marshmallow


class MangaSchema(marshmallow.Schema):
    class Meta:
        fields = (
            'id', 'title', 'status', 'description', 'genres', 'url', 'thumbnail_url', 'manhwa', 'favourite', 'added')


manga_schema = MangaSchema()
mangas_schema = MangaSchema(many=True)