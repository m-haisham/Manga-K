from whaaaaat import prompt

def confirm(message, default=True):
    return prompt(dict(
        type='confirm',
        name='q',
        message=message,
        default=default
    ))['q']