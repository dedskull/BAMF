import bin_parse_module
import yara
import common
import re


class pbot(bin_parse_module.PHPParseModule):
    def __init__(self):
        bin_parse_module.PHPParseModule.__init__(self, "pBot")
        self.yara_rules = None
        pass

    def _generate_yara_rules(self):
        if self.yara_rules is None:
            self.yara_rules = yara.compile(
                source='rule pbot_config { '
                       'strings: $config = "var $config = array" $c = "class pBot" '
                       'condition: all of them }')
        return self.yara_rules

    def get_config_values(self, config):
        try:
            p = re.compile(r'[\'"](?P<key>[^\'"]+)[\'"][\s]*=>[\s]*[\'"](?P<value>[^\'"]+)[\'"]', re.MULTILINE)
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
            p = re.compile(r'var[\s]+\$config[\s]*=[\s]*array[\s]*\([\s]*(\"[^\"]*\"[\s]*=>.*,?[\s]*)*(//)?\);', re.MULTILINE)
            result = p.search(file_data)
            if result == None:
                return {}
            ret = self.get_config_values(result.group(0))
        except:
            pass
        return ret

common.Modules.list.append(pbot())