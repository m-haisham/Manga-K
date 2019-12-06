class Catch:
    """
    Using this decorator around an function which gives a return may cause it to not give a return if error is thrown
    """
    def __init__(self, *, error_type=KeyboardInterrupt, output=False):
        self.error_type = error_type
        self.output = output

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            r = None
            try:
                r = func(*args, **kwargs)
            except self.error_type as e:
                if self.output:
                    print(e)
            return r

        return wrapper