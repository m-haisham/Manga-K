from flask_restful import Api


class Rest:
    _instance = None

    def __init__(self, app):
        self.app = app
        self.api = Api(self.app)

    @staticmethod
    def set(app):
        """
        creates new api from :param app: and sets it to instance

        :return: None
        """
        if Rest._instance is None:
            Rest._instance = Rest(app)

    @staticmethod
    def get():
        """
        :return: rest api instance
        """
        return Rest._instance
