from modules.console.menu import Menu
from .refresh import refresh
from .reset import reset
from .favourites import favourites
from .updates import updates

def menu():
    Menu("What would you like to do?", {
        'Updates': updates,
        'Favourites': favourites,
        Menu.seperator(' '): '',
        'Refresh': refresh,
        'Erase data': reset
    }).prompt()
