import cStringIO
import pycurl
import urllib


class Modules:
    list = []

    def __init__(self):
        pass


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


class BruteModule(object):
    def __init__(self, metadata, data_type):
        self.data_type = data_type
        self.metadata = metadata

    def get_metadata(self):
        return self.metadata

    def get_module_name(self):
        return self.metadata.module_name

    def get_bot_name(self):
        return self.metadata.bot_name

    def try_credentials(self, credentials):
        return False


class HTTPBruteModule(BruteModule):
    def __init__(self, metadata):
        BruteModule.__init__(self, metadata, "HTTP")

    def check_page_is_valid(self, uri):
        return False


class WebRequests(object):
    proxy_host = None
    proxy_port = None
    proxy_type = pycurl.PROXYTYPE_SOCKS5
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0'

    @staticmethod
    def get_request(uri, arguments=None):
        headers = cStringIO.StringIO()
        body = cStringIO.StringIO()
        c = pycurl.Curl()
        if arguments is None:
            c.setopt(c.URL, uri)
        else:
            params = urllib.urlencode(arguments)
            c.setopt(c.URL, "%s?%s" % (uri, params))
        c.setopt(c.HEADERFUNCTION, headers.write)
        c.setopt(c.WRITEFUNCTION, body.write)
        c.setopt(pycurl.USERAGENT, WebRequests.user_agent)
        if WebRequests.proxy_host is not None and WebRequests.proxy_port is not None and \
                WebRequests.proxy_type is not None:
            c.setopt(pycurl.PROXY, WebRequests.proxy_host)
            c.setopt(pycurl.PROXYPORT, WebRequests.proxy_port)
            c.setopt(pycurl.PROXYTYPE, WebRequests.proxy_type)
        c.perform()

        return c.getinfo(pycurl.HTTP_CODE), headers.getvalue(), body.getvalue()

    @staticmethod
    def post_request(uri, arguments):
        headers = cStringIO.StringIO()
        body = cStringIO.StringIO()
        c = pycurl.Curl()
        params = urllib.urlencode(arguments)
        c.setopt(c.URL, uri)
        c.setopt(c.POSTFIELDS, params)
        c.setopt(c.HEADERFUNCTION, headers.write)
        c.setopt(c.WRITEFUNCTION, body.write)
        c.setopt(pycurl.USERAGENT, WebRequests.user_agent)
        if WebRequests.proxy_host is not None and WebRequests.proxy_port is not None and \
                WebRequests.proxy_type is not None:
            c.setopt(pycurl.PROXY, WebRequests.proxy_host)
            c.setopt(pycurl.PROXYPORT, WebRequests.proxy_port)
            c.setopt(pycurl.PROXYTYPE, WebRequests.proxy_type)
        c.perform()

        return c.getinfo(pycurl.HTTP_CODE), headers.getvalue(), body.getvalue()