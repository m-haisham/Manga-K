from marshmallow import Schema, fields
from ..manga import MangaSchema
from ..chapter import ChapterSchema


class DetailedUpdateSchema(Schema):
    manga = fields.Nested(MangaSchema)
    chapter = fields.Nested(ChapterSchema(exclude=('update',)))

    class Meta:
        fields = ('id', 'time', 'manga', 'chapter')


updates_schema = DetailedUpdateSchema(many=True)