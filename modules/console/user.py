from .confirm import confirm
from .display import format_dict_pair


def from_template(template):
    if type(template) == dict:

        result = {}
        for key in template.keys():
            if type(template[key]) == bool:
                result[key] = confirm(key, default=template[key])

        return result