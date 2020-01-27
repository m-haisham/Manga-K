from flask_restful import Api


class Rest:
    _instance = None

    def __init__(self, app):
        self.app = app
        self.api = Api(self.app)

    @staticmethod
    def set(app):
        if Rest._instance is None:
            Rest._instance = Rest(app)

    @staticmethod
    def get():
        return Rest._instance
