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
    api.add_resource(Manga, '/manga/<int:manga_id>')
    api.add_resource(Updates, '/updates/<int:manga_id>')
    api.add_resource(Thumbnail, '/thumbnail/<int:manga_id>')
    api.add_resource(Chapter, '/chapter/<manga_id>/<chapter_id>')
    api.add_resource(PageList, '/pages/<manga_id>/<chapter_id>')
    api.add_resource(Page, '/page/<manga_id>/<chapter_id>/<int:i>')

    api.add_resource(FavouriteList, '/favourites')
    api.add_resource(RecentList, '/recents')

    api.add_resource(Search, '/search/<int:i>')
    api.add_resource(Popular, '/popular', '/popular/<int:i>')
    api.add_resource(Latest, '/latest', '/latest/<int:i>')

    api.add_resource(DownloadsList, '/downloads')
    api.add_resource(Download, '/download/<int:i>')
    api.add_resource(DownloadStatus, '/downloads/status')
    api.add_resource(DownloadDelete, '/downloads/delete')
