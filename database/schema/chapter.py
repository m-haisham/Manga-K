from marshmallow import Schema, fields
from .update import UpdateSchema


class ChapterSchema(Schema):
    update = fields.Nested(UpdateSchema, missing=None)

    class Meta:
        fields = ('id', 'title', 'url', 'update_status', 'read', 'downloaded', 'manga_id', 'added', 'update')


chapter_schema = ChapterSchema()
chapters_schema = ChapterSchema(many=True)
