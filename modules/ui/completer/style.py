from colorama import Fore


class CompleterStyle:
    def __init__(self, prefix='[', postfix=']', success=Fore.GREEN, error=Fore.RED, info=Fore.BLUE):
        self.prefix = prefix
        self.postfix = postfix
        self.success = success
        self.error = error
        self.info = info
