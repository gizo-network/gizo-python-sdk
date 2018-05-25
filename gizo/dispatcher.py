from furl import furl
class Dispatcher:
    def __init__(self, url: str=None):
        self.url = url
        self.pub = None
        self.ip = None
        self.port = None
        parsed = furl(url)
        if parsed.username != None and parsed.host != None and parsed.port != None:
            self.pub = parsed.username
            self.ip = parsed.host
            self.port = parsed.port        
        else:
            raise Exception("Unable to parse input url")

    def rpc(self):
        return "http://{}:{}/rpc".format(self.ip, self.port)