import bin_parse_module
import yara
import common
import base64


class madness_pro(bin_parse_module.PEParseModule):
    def __init__(self):
        bin_parse_module.PEParseModule.__init__(self, "Madness Pro")
        self.yara_rules = None
        pass

    def _generate_yara_rules(self):
        if self.yara_rules is None:
            self.yara_rules = yara.compile(
                source='rule config { strings: $c = "YXBvS0FMaXBsaXM9" $str5 = "d3Rm" fullword '
                       '$str6 = "ZXhl" fullword condition: all of them }')
        return self.yara_rules

    @staticmethod
    def bdecode(key):
        key = key.replace("^", "j")
        key = key.replace("@", "H")
        key = key.replace("*", "d")
        key = base64.b64decode(key)
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
        for s in common.data_strings(file_data):
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

common.Modules.list.append(madness_pro())