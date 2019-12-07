from .confirm import confirm
from .input import vinput as validated_input


def from_template(template):
    if type(template) == dict:

        result = {}
        for key in template.keys():
            if type(template[key]) == bool:
                result[key] = confirm(key, default=template[key])
            elif type(template[key]) == int or template[key] == 0:
                result[key] = validated_input(key, default=template[key], input_type=int)

        return result