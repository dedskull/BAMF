from common import Modules, load_yara_rules, PHPParseModule
from re import compile as recompile, MULTILINE


class pbot(PHPParseModule):
    def __init__(self):
        PHPParseModule.__init__(self, "pBot")
        self.yara_rules = None
        pass

    def _generate_yara_rules(self):
        if self.yara_rules is None:
            self.yara_rules = load_yara_rules("pbot.yara")
        return self.yara_rules

    def get_config_values(self, config):
        try:
            p = recompile(r'[\'"](?P<key>[^\'"]+)[\'"][\s]*=>[\s]*[\'"](?P<value>[^\'"]+)[\'"]', MULTILINE)
            results = p.findall(config)
            ret = {}
            for pair in results:
                ret[pair[0]] = pair[1]
            return ret
        except:
            return {}

    def get_bot_information(self, file_data):
        ret = {}
        try:
            p = recompile(r'var[\s]+\$config[\s]*=[\s]*array[\s]*\([\s]*(\"[^\"]*\"[\s]*=>.*,?[\s]*)*(//)?\);', MULTILINE)
            result = p.search(file_data)
            if result is None:
                return {}
            ret = self.get_config_values(result.group(0))
        except:
            pass
        return ret

Modules.list.append(pbot())