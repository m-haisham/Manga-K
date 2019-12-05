from colorama import init, Fore
from colorama.ansi import AnsiFore

init()


def colored(s: str, fore: str or AnsiFore = Fore.RESET):
    if type(s) != str:
        raise TypeError('"s" must be a string')

    if not (type(fore) == AnsiFore or type(fore) == str):
        raise TypeError(f'"fore" {type(fore)} must be a AnsiFore or str')

    return f'{fore}{s}{Fore.RESET}'


print_colored = lambda s, fore: print(colored(s, fore))

red = lambda s: colored(s, Fore.RED)
blue = lambda s: colored(s, Fore.BLUE)
green = lambda s: colored(s, Fore.GREEN)
