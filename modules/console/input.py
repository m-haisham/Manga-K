from whaaaaat import prompt
from whaaaaat import ValidationError, Validator


def vinput(message, default=True, input_type=str):

    class TypeValidator(Validator):
        def validate(self, document):
            try:
                input_type(document.text)
            except Exception as e:
                print(e)
                raise ValidationError(
                    message=f'please enter a valid {input_type}',
                    cursor_position=len(document.text)
                )

    if type(default) != str:
        default = str(default)

    return prompt(dict(
        type='input',
        name='q',
        message=message,
        default=default,
        validate=TypeValidator
    ))['q']

