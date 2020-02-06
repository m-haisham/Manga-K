from .exceptions import NetworkError
from .helper import NetworkHelper


def checked_connection(func):
    """
    checks for internet connection before executing

    :param func: function to execute
    :raises NetworkError: if internet connection cannot be established
    """
    def wrapper(*args, **kwargs):
        connected = NetworkHelper.is_connected()
        if not connected:
            raise NetworkError('Failed to establish a connection')

        out = func(*args, **kwargs)
        return out

    return wrapper
