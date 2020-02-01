from ..rest import Rest
from .manga import Manga, MangaList
from .favourite import FavouriteList
from .chapter import Chapter
from .page import Page, PageList

from .search import Search
from .popular import Popular
from .latest import Latest
from .download import Download, DownloadsList, DownloadStatus, DownloadDelete
from .recent import RecentList
from .update import Updates
from .thumbnail import Thumbnail


def setup():
    # init
    api = Rest.get().api

    # setup
    api.add_resource(MangaList, '/mangas')
    api.add_resource(Manga, '/manga/<manga_slug>')
    api.add_resource(Updates, '/manga/<manga_slug>/updates')
    api.add_resource(Thumbnail, '/manga/<manga_slug>/thumbnail')
    api.add_resource(Chapter, '/manga/<manga_slug>/<chapter_slug>')
    api.add_resource(PageList, '/manga/<manga_slug>/<chapter_slug>/pages')
    api.add_resource(Page, '/manga/<manga_slug>/<chapter_slug>/<int:i>')

    api.add_resource(FavouriteList, '/favourites')
    api.add_resource(RecentList, '/recents')

    api.add_resource(Search, '/search/<int:i>')
    api.add_resource(Popular, '/popular', '/popular/<int:i>')
    api.add_resource(Latest, '/latest', '/latest/<int:i>')

    api.add_resource(DownloadsList, '/downloads')
    api.add_resource(Download, '/download/<int:i>')
    api.add_resource(DownloadStatus, '/downloads/status')
    api.add_resource(DownloadDelete, '/downloads/delete')
