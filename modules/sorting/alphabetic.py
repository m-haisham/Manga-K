import string

from whaaaaat import Separator


def sort_initials(objects, key=None, key_modifier=lambda val: val.upper()):
    if key is None:
        key = lambda val: val

    separated = {}

    for obj in objects:

        val = key(obj)

        if type(val) != str:
            continue
        if len(val) <= 0:
            continue
        if val[0].lower() in string.ascii_lowercase:
            k = val[0]
        else:
            k = '#'

        # apply modifier
        k = key_modifier(k)

        if k not in separated.keys():
            separated[k] = []

        separated[k].append(obj)

    return separated


def alphabetic_prompt_list(l, key=lambda val: val):
    alphabetic = sort_initials(l, key=key)
    sorted_keys = sorted(alphabetic.keys())

    sorted_list = []
    for key in sorted_keys:
        if len(sorted_list) != 0:
            sorted_list.append(Separator(' '))
        sorted_list.append(Separator(key))

        # sort the sublist and add to sorted list
        sorted_list.extend(sorted(alphabetic[key]))

    return sorted_list