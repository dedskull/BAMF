from string import printable


class Modules:
    list = []


def data_strings(data, min=4):
    result = ""
    for c in data:
        if c in printable:
            result += c
            continue
        if len(result) >= min:
            yield result
        result = ""