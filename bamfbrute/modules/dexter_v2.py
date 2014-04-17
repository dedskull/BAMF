from common import HTTPBruteModule, ModuleMetadata, WebRequests, Modules


class dexter_v2(HTTPBruteModule):
    def __init__(self):
        md = ModuleMetadata(
            module_name="dexter_v2",
            bot_name="Dexter v2",
            description="Point of sale malware designed to extract credit card information from RAM",
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
        if r[0] != 200:
            return False
        return r[2].find('Please disable your SOCKS,Proxy or VPN and try again.') == -1

    def check_page_is_valid(self, uri):
        return WebRequests.post_request(uri,
                                        {"username": False,
                                         "password": False,
                                         "submit": True})[2].find("Author: Boutsakis Vagelis (boutsak@gmail.com)") != -1

Modules.list.append(dexter_v2())
