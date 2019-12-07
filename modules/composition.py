from pathlib import Path

from tqdm import tqdm
from whaaaaat import prompt

from .ImageStacking import dir_to_pdf, dir_to_img
from .static import Const, is_any_manga_downloaded

composing_options = {
    Const.PdfDIr: dir_to_pdf,
    Const.JpgDir: dir_to_img
}


def compose_menu():
    if not is_any_manga_downloaded(True):
        return

    compose_menu_options = {
        'type': 'list',
        'name': 'compose',
        'message': 'Pick composition type.',
        'choices': [str(key) for key in composing_options.keys()]
    }

    response = ''
    try:
        response = prompt(compose_menu_options)['compose']
        response = Path(response)
    except KeyError as e:
        print(e)

    manga, chapters = chapterSelection()
    (manga / Path(response)).mkdir(exist_ok=True)

    for chapter in tqdm(chapters):
        composing_options[response](
            chapter,
            manga / Path(response)
        )


def chapterSelection():
    """
    :returns array os strings pointing to chapters to be composed
    """

    manga_dir = Path(Const.MangaSavePath)

    mangas = list(manga_dir.iterdir())
    if len(mangas) <= 0:
        return Path, []

    # manga selection
    manga_options = {
        'type': 'list',
        'name': 'manga',
        'message': 'Pick manga',
        'choices': map(lambda path: path.parts[-1], mangas),
        'filter': lambda val: mangas[mangas.index(Path(Const.MangaSavePath) / Path(val))]
    }

    manga: Path = Path()
    try:
        manga = prompt(manga_options)['manga']
        manga = Path(manga)
    except KeyError as e:
        print(e)
        return Path, []

    # select chapters
    chapter_option = {
        'type': 'checkbox',
        'name': 'chapters',
        'message': 'Select chapters to compose',
        'choices': [{'name': i.parts[-1]} for i in manga.iterdir() if not is_folder_static(i.parts[-1])],
    }

    # if no chapters
    if len(chapter_option['choices']) <= 0:
        return manga, []

    chapters = []
    try:
        chapters = prompt(chapter_option)['chapters']
        chapters = map(lambda path: manga / Path(path), chapters)
    except KeyError as e:
        print(e)
        return manga, []

    return manga, list(chapters)


def is_folder_static(folder_name) -> bool:
    return folder_name == Const.StructFile or folder_name == Const.JpgDir or folder_name == Const.PdfDIr
