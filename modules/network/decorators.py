from .helper import NetworkHelper
from .exceptions import NetworkError


def checked_connection(func):
    def wrapper(*args, **kwargs):
        connected = NetworkHelper.is_connected()
        if not connected:
            raise NetworkError('Failed to establish a connection')

        out = func(*args, **kwargs)
        return out

    return wrapper
