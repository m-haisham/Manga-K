from marshmallow import Schema, fields


class UpdateSchema(Schema):
    class Meta:
        fields = ('id', 'time', 'manga_id', 'chapter_id')


update_schema = UpdateSchema()
