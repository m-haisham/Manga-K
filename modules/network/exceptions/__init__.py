class NetworkError(Exception):
    def __call__(self, message, *args, **kwargs):
        super(NetworkError, self).__call__(message)


class IdentificationError(Exception):
    def __call__(self, message, *args, **kwargs):
        super(IdentificationError, self).__call__(message)
