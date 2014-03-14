from common import Modules, data_strings, load_yara_rules, PEParseModule
from base64 import b64decode


class madness_pro(PEParseModule):
    def __init__(self):
        PEParseModule.__init__(self, "Madness Pro")
        self.yara_rules = None
        pass

    def _generate_yara_rules(self):
        if self.yara_rules is None:
            self.yara_rules = load_yara_rules("madnesspro.yara")
        return self.yara_rules

    @staticmethod
    def bdecode(key):
        key = key.replace("^", "j")
        key = key.replace("@", "H")
        key = key.replace("*", "d")
        key = b64decode(key)
        return key

    @staticmethod
    def parse_madness_pro_config(key):
        key = madness_pro.bdecode(key)
        key = key[len("apoKALiplis=uebok"):]
        if key[0] == key[1] == key[2]:
            tkey = ""
            for x in range(0, len(key)):
                if x % 3 == 0:
                    tkey += key[x]
            key = tkey
        return key[:-len("0fe9bdh")]

    def get_bot_information(self, file_data):
        results = {}
        for s in data_strings(file_data):
            if s[:len("YXBvS0")] == "YXBvS0":
                results["c2_uri"] = madness_pro.parse_madness_pro_config(s)
            else:
                try:
                    ret = madness_pro.bdecode(s)
                    if ret[:2][1:] == ".":
                        results["version"] = ret
                except:
                    pass
        return results

Modules.list.append(madness_pro())