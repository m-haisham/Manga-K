from flask_restful import Resource
from modules import favourite
from ..encoding import linked_dict


class Favourite(Resource):
    def get(self):
        return dict(manga=[linked_dict(manga) for manga in favourite.all()])
