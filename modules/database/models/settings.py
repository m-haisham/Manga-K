from modules.console import format_dict_pair, from_template


class Settings:
    def __init__(
            self,
            pdf=False,
            jpg=False,
            disable_downloaded=True,
            image_separation=10
    ):
        self.pdf = pdf
        self.jpg = jpg
        self.disable_downloaded = disable_downloaded
        self.image_separation = image_separation

    def display(self):
        settings = self.todict()

        for key in settings.keys():
            print(format_dict_pair(key, settings[key]))

    def todict(self):
        return vars(self)

    def is_compositing(self):
        return any([
            self.pdf,
            self.jpg
        ])

    @staticmethod
    def prompt():
        return Settings.fromdict(from_template(Settings().todict()))

    @staticmethod
    def fromdict(d: dict):
        assert isinstance(d, dict)

        try:
            s = Settings()
            for key in d.keys():
                setattr(s, key, d[key])

            return s
        except KeyError:
            return
