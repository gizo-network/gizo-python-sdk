class Dispatcher:
    def __init__(self, pub=None, ip=None, port=None):
        self.pub = pub
        self.ip = ip
        self.port = port
    def getPub(self):
        return self.pub
    def setPub(self, pub):
        self.pub = pub
    def __getIP(self): 
        return self.ip
    def setIP(self, ip):
        self.ip = ip
    def __getPort(self):
        return self.port
    def setPort(self, port):
        self.port = port
    def url(self):
        return "http://{}:{}/rpc".format(self.__getIP(), self.__getPort())