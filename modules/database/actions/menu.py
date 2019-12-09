from modules.console.menu import Menu
from .refresh import refresh
from .reset import reset
from .favourites import favourites

def menu():
    Menu("What would you like to do?", {
        'Favourites': favourites,
        Menu.seperator(' '): '',
        'Refresh': refresh,
        'Erase data': reset
    }).prompt()
