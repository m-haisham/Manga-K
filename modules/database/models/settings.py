from modules.console import format_dict_pair, from_template


class Settings:
    def __init__(
            self,
            pdf=False,
            jpg=False
    ):
        self.pdf = pdf
        self.jpg = jpg

    def display(self):
        settings = self.to_dict()

        for key in settings.keys():
            print(format_dict_pair(key, settings[key]))

    def to_dict(self):
        return vars(self)

    @staticmethod
    def prompt():
        return Settings.from_dict(from_template(Settings().to_dict()))

    @staticmethod
    def from_dict(d: dict):
        assert isinstance(d, dict)

        try:
            return Settings(d['pdf'], d['jpg'])
        except KeyError:
            return
