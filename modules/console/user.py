from .confirm import confirm


def from_template(template):
    if type(template) == dict:

        result = {}
        for key in template.keys():
            if type(template[key]) == bool:
                result[key] = confirm(key, default=template[key])

        return result