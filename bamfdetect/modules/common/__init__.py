from string import printable
from yara import compile
from os.path import dirname, join, abspath


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


def load_yara_rules(name):
    return compile(join(dirname(abspath(__file__)), "..", "yara", name))