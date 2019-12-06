from whaaaaat import prompt


def input(message, default=True):
    return prompt(dict(
        type='input',
        name='q',
        message=message,
        default=default
    ))['q']


