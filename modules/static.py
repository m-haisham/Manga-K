from pathlib import Path

from modules.ui.colorize import red


class Const:
    MangaSavePath = Path('Manga')
    StyleSaveFile = Path('style.css')
    StructFile = 'tree.json'

    PdfDIr = Path('pdf')
    JpgDir = Path('jpg')


def is_any_manga_downloaded(verbose=False) -> bool:
    manga_path = Path(Const.MangaSavePath)

    is_downloaded = manga_path.exists() and manga_path.is_dir() and len(list(manga_path.iterdir())) > 0
    if verbose and not is_downloaded:
        print(f'[{red("X")}] No mangas downloaded')

    return is_downloaded
