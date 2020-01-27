from flask_restful import Resource
from modules.database import mangadata

from ..encoding import linked_dict, UrlEncoding


class Manga(Resource):
    def get(self, title=None):

        if title is None:
            # return all the manga

            return {
                'manga': [linked_dict(table.get_info()) for table in mangadata.all()]
            }
        else:
            try:
                title = UrlEncoding.back(title)
                table = mangadata.databases[title]

                manga = linked_dict(table.get_info())

                manga['chapters'] = table.chapters.all()

                return manga
            except KeyError:
                pass
