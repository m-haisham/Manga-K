from .regex import numbers, floating


def numerical_sort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def floating_sort(value):
    parts = floating.split(value)
    parts[1::2] = map(float, parts[1::2])
    return parts[1::2]
