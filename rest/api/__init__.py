from ..rest import Rest
from .manga import Manga, MangaList
from .favourite import FavouriteList
from .chapter import Chapter
from .page import Page

from .search import Search
from .popular import Popular
from .latest import Latest
from .download import Download, DownloadsList, DownloadStatus


def setup():
    # init
    api = Rest.get().api

    # setup
    api.add_resource(MangaList, '/mangas')
    api.add_resource(FavouriteList, '/favourites')
    api.add_resource(Manga, '/manga/<title>')
    api.add_resource(Chapter, '/manga/<manga_title>/<chapter_title>')
    api.add_resource(Page, '/manga/<manga_title>/<chapter_title>/<int:i>')

    api.add_resource(Search, '/search/<int:i>')
    api.add_resource(Popular, '/popular', '/popular/<int:i>')
    api.add_resource(Latest, '/latest', '/latest/<int:i>')

    api.add_resource(DownloadsList, '/downloads')
    api.add_resource(Download, '/download/<int:i>')
    api.add_resource(DownloadStatus, '/download/status')
