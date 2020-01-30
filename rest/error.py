def error_message(message, **kwargs):
    out = {'message': message}

    for key, value in kwargs.items():
        out[key] = value

    return out
