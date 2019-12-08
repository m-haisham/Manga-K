from whaaaaat import prompt, Separator


class Menu:
    def __init__(self, message, options, return_index=False, action=True, key=lambda val: val):
        """

        :param options: key-action pairs
        :param action:
        :param loop:
        """
        self.return_index = return_index
        self.message = message
        self.action = action

        if type(options) == list:
            self._options = {}
            for option in options:
                if type(option) == str:
                    self._options[option] = ''
                else:
                    self._options[key(option)] = ''
            self.action = False
        else:
            self._options = options

    @property
    def options(self):
        return self._options

    def loop(self, condition=True):
        while condition:
            self.prompt()

    def prompt(self):

        key = prompt(dict(
            type='list',
            name='dialog',
            message=self.message,
            choices=list(self.options.keys())
        ))['dialog']

        if self.return_index:
            for i, k in enumerate(self.options.keys()):
                if i == k:
                    return i
        elif self.action:
            self.options[key]()
        else:
            return key

    @staticmethod
    def seperator(s=''):
        return Separator(s)