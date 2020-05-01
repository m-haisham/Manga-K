from flask_restful import Resource

from database import LocalSession
from database.access import MangaAccess
from database.models import UpdateModel

from database.schema.update.many import updates_schema

from ..request import limit_parser

class Updates(Resource):
    def get(self, manga_id):
        # get information
        access = MangaAccess(manga_id)

        model = access.get_or_404()

        return updates_schema.dump(model.updates)


class UpdatesList(Resource):
    def get(self):
        args = limit_parser.parse_args()
        if args['limit'] is None:
            updates = LocalSession.session.query(UpdateModel).order_by(UpdateModel.time.desc()).all()
        else:
            updates = LocalSession.session.query(UpdateModel).order_by(UpdateModel.time.desc()).limit(args['limit']).all()

        return updates_schema.dump(updates)
