import marshmallow


class RecentSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'time', 'manga_id', 'chapter_id')


recent_schema = RecentSchema()
recents_schema = RecentSchema(many=True)
