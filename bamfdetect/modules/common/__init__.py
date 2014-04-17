from string import printable
from yara import compile
from os.path import dirname, join, abspath


class ModuleMetadata(object):
    def __init__(self, module_name, bot_name, description, authors, date, version, references):
        self.module_name = module_name
        self.bot_name = bot_name
        self.description = description
        self.authors = authors
        self.date = date
        self.version = version
        self.references = references

    def __str__(self):
        return "%s (%s %s) - %s" % (self.bot_name, self.module_name, self.version, self.description)


class BinParseModule(object):
    def __init__(self, metadata, data_type):
        self.data_type = data_type
        self.metadata = metadata

    def get_metadata(self):
        return self.metadata

    def get_module_name(self):
        return self.metadata.module_name

    def get_bot_name(self):
        return self.metadata.bot_name

    def _generate_yara_rules(self):
        return None

    def is_bot(self, file_data):
        rules = self._generate_yara_rules()
        if rules is None:
            return None
        return len(rules.match(data=file_data)) != 0

    def get_bot_information(self, file_data):
        return None


class PEParseModule(BinParseModule):
    def __init__(self, metadata):
        BinParseModule.__init__(self, metadata, "PE")


class PHPParseModule(BinParseModule):
    def __init__(self, metadata):
        BinParseModule.__init__(self, metadata, "PHP")


class Modules:
    list = []


def data_strings(data, min=4, charset=printable):
    result = ""
    for c in data:
        if c in charset:
            result += c
            continue
        if len(result) >= min:
            yield result
        result = ""
    if len(result) >= min:
        yield result


def load_yara_rules(name):
    return compile(join(dirname(abspath(__file__)), "..", "yara", name))