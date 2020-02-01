
def mkdir(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.mkdir(parents=True, exist_ok=True)

        return response

    return wrapper