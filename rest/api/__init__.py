from ..rest import Rest
from .manga import Manga, MangaList
from .favourite import FavouriteList
from .chapter import Chapter

def setup():
    # init
    api = Rest.get().api

    # setup
    api.add_resource(MangaList, '/mangas')
    api.add_resource(FavouriteList, '/favourites')
    api.add_resource(Manga, '/manga/<title>')
    api.add_resource(Chapter, '/manga/<manga_title>/<chapter_title>')