import os
from pathlib import Path

from modules.ui import unicode
from modules.ui.colorize import red, green


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


def visualize(val) -> str:
    """
    :returns appropriate symbol for the input colorized
    """
    if type(val) == bool:
        if val:
            return green(unicode.CHECK_MARK)
        else:
            return red('X')
    else:
        return val


def is_any_manga_downloaded(verbose=False) -> bool:
    manga_path = Path(Const.MangaSavePath)

    is_downloaded = manga_path.exists() and manga_path.is_dir() and len(list(manga_path.iterdir())) > 0
    if verbose and not is_downloaded:
        print(f'[{red("X")}] No mangas downloaded')

    return is_downloaded
