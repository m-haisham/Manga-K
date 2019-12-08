from modules.console.menu import Menu
from .refresh import refresh

def menu():
    Menu("What would you like to do?", dict(
        refresh=refresh
    )).prompt()