from modules import favourite
from modules.database.models.manga.dialog import MangaDialog
from modules.database.models import Manga
from modules.sorting.alphabetic import alphabetic_prompt_list
from modules.console.menu import Menu

def favourites():
    # get all favourites
    favoured = alphabetic_prompt_list(favourite.all(), key=lambda val: val.title)

    options = {}
    for item in favoured:
        if isinstance(item, Manga):
            options[item.title] = lambda: MangaDialog(item).prompt()
        else:
            options[item] = ''

    Menu('Select', options).prompt()
