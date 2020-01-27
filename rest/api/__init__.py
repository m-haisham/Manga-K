from ..rest import Rest
from .manga import Manga
from .favourite import Favourite


def setup():
    # init
    api = Rest.get().api

    # setup
    api.add_resource(Manga, '/manga', '/manga/<title>')
    api.add_resource(Favourite, '/favourite')
