import marshmallow


class ChapterSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'title', 'url', 'read', 'downloaded', 'manga_id', 'added')


chapter_schema = ChapterSchema()
chapters_schema = ChapterSchema(many=True)
