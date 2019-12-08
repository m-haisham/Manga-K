from modules.console.menu import Menu
from .refresh import refresh
from .reset import reset

def menu():
    Menu("What would you like to do?", {
        'Refresh': refresh,
        Menu.seperator(' '): '',
        'Erase data': reset
    }).prompt()