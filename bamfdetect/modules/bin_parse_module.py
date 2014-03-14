class BinParseModule(object):
    def __init__(self, name, data_type):
        self.data_type = data_type
        self.name = name

    def get_name(self):
        return self.name

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
    def __init__(self, name):
        BinParseModule.__init__(self, name, "PE")


class PHPParseModule(BinParseModule):
    def __init__(self, name):
        BinParseModule.__init__(self, name, "PHP")