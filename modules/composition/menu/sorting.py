from whaaaaat import Separator

from modules.sorting import sort_initials


def alphabetric_list(l):
    alphabetic = sort_initials(l)
    sorted_keys = sorted(alphabetic.keys())

    sorted_list = []
    for key in sorted_keys:
        if len(sorted_list) != 0:
            sorted_list.append(Separator(' '))
        sorted_list.append(Separator(key))

        # sort the sublist and add to sorted list
        sorted_list.extend(sorted(alphabetic[key]))

    return sorted_list