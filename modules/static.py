from pathlib import Path

from modules.ui import unicode
from modules.ui.colorize import red, green


class Const:
    MangaSavePath = Path('Manga')
    StyleSaveFile = Path('style.css')
    StructFile = 'tree.json'

    PdfDIr = Path('pdf')
    JpgDir = Path('jpg')

    @staticmethod
    def create_manga_save():
        Const.MangaSavePath.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def createCompositionDirs(manga_dir):
        if type(manga_dir) == str:
            manga_dir = Path(manga_dir)

        (manga_dir / Const.PdfDIr).mkdir(exist_ok=True, parents=True)
        (manga_dir / Const.JpgDir).mkdir(exist_ok=True, parents=True)


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
