import marshmallow


class RecentSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'time', 'manga_id', 'chapter_id')


recents_schema = RecentSchema(many=True)
