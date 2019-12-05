import os
from pathlib import Path

from . import unicode
from .colorize import red


class Const:
    MangaSavePath = 'Manga'
    StyleSaveFile = 'style.css'
    StructFile = 'tree.json'

    PdfDIr = 'pdf'
    JpgDir = 'jpg'

    @staticmethod
    def createCompositionDirs(manga_dir):
        if not os.path.exists(os.path.join(manga_dir, Const.PdfDIr)):
            os.mkdir(os.path.join(manga_dir, Const.PdfDIr))
        if not os.path.exists(os.path.join(manga_dir, Const.JpgDir)):
            os.mkdir(os.path.join(manga_dir, Const.JpgDir))


def is_any_manga_downloaded(verbose=False) -> bool:

    manga_path = Path(Const.MangaSavePath)

    is_downloaded = manga_path.exists() and manga_path.is_dir() and len(list(manga_path.iterdir())) > 0
    if verbose and not is_downloaded:
        print(f'[{red("X")}] No mangas downloaded')

    return is_downloaded
