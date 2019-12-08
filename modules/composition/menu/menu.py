from pathlib import Path

from tqdm import tqdm
from whaaaaat import prompt

from modules import database
from modules.composition.pdf import dir_to_pdf
from modules.composition.jpg import dir_to_jpg
from modules.database.models import Manga
from modules.sorting import numerical_sort
from modules.ui.colorize import red
from ..dir import directories
from .sorting import alphabetric_list

composing_options = {
    directories.pdf.parts[-1]: dir_to_pdf,
    directories.jpg.parts[-1]: dir_to_jpg
}


def compose_menu():
    if len(database.manga.all()) <= 0:
        print(f'[{red("X")}] No mangas downloaded')
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
        composing_options[response.parts[-1]](
            chapter,
            manga / response
        )


def chapterSelection():
    """
    :returns array os strings pointing to get_chapter_list to be composed
    """

    manga_dir = Manga.directory

    mangas = list(manga_dir.iterdir())
    if len(mangas) <= 0:
        return Path, []

    # manga selection
    manga_options = {
        'type': 'list',
        'name': 'manga',
        'message': 'Pick manga',
        'choices': alphabetric_list(map(lambda path: path.parts[-1], mangas)),
        'filter': lambda val: mangas[mangas.index(Manga.directory / Path(val))]
    }

    manga: Path = Path()
    try:
        manga = prompt(manga_options)['manga']
        manga = Path(manga)
    except KeyError as e:
        print(e)
        return Path, []

    # select get_chapter_list
    chapter_option = {
        'type': 'checkbox',
        'name': 'get_chapter_list',
        'message': 'Select get_chapter_list to compose',
        'choices': sorted(
            [{'name': i.parts[-1]} for i in manga.iterdir() if not is_folder_static(i.parts[-1])],
            key=lambda val: numerical_sort(val['name'])
        ),
    }

    # if no get_chapter_list
    if len(chapter_option['choices']) <= 0:
        return manga, []

    try:
        chapters = prompt(chapter_option)['get_chapter_list']
        chapters = map(lambda path: manga / Path(path), chapters)
    except KeyError as e:
        print(e)
        return manga, []

    return manga, list(chapters)


def is_folder_static(folder_name) -> bool:
    return folder_name in composing_options.keys()