from ..regex import floating_matcher


def extract_float(s):
    """
    Extracts all the floating point values from value
    :param s: string to match
    :return: list of floating points
    :rtype: list
    """
    numbers = floating_matcher.findall(s)
    return numbers
