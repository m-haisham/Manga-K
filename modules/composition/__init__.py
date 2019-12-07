from pathlib import Path

from modules.empty import Namespace
from .menu import compose_menu
from .jpg import dir_to_jpg
from .pdf import dir_to_pdf

directories = Namespace()
setattr(directories, 'jpg', Path('jpg'))
setattr(directories, 'pdf', Path('pdf'))


def create_directories(manga):
    dir = vars(directories)
    for key in dir.keys():
        (manga.path() / dir[key]).mkdir(exist_ok=True, parents=True)
