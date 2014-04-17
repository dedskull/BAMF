from common import HTTPBruteModule, ModuleMetadata, WebRequests, Modules


class madnesspro_v114(HTTPBruteModule):
    def __init__(self):
        md = ModuleMetadata(
            module_name="madnesspro_v114",
            bot_name="Madness Pro v114",
            description="Distributed Denial of Service botnet capable of various attacks",
            authors=["Brian Wallace (@botnet_hunter)"],
            version="1.0.0",
            date="March 26, 2014",
            references=[]
        )
        HTTPBruteModule.__init__(self, md)

    def try_credentials(self, credentials):
        if 'uri' not in credentials or 'username' not in credentials or 'password' not in credentials:
            raise Exception("Not enough values were defined")
        r = WebRequests.post_request(credentials['uri'], {"username": credentials['username'],
                                                          "password": credentials['password'],
                                                          "submit": True})
        if r[0] != 302:
            return False
        return r[1].find('Location: index.php') != -1

    def check_page_is_valid(self, uri):
        return WebRequests.get_request(uri)[2].find('<p align=\"center\"><img src=\"./img/madness.png\" border=\"0\">')\
            != -1

Modules.list.append(madnesspro_v114())