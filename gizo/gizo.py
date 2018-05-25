import requests
import hprose
import json
import gizo.const as const
from furl import furl
from gizo.dispatcher import Dispatcher

class Gizo:
    def __init__(self, url: str =None):
        self.__dispatcher: Dispatcher = None
        self.__client = None
        if url is not None:
            parsed = furl(url)
            if parsed.username != None and parsed.host != None and parsed.port != None:
                self.__dispatcher = Dispatcher(parsed.username, parsed.host, parsed.port)
            else:
                raise Exception("Unable to parse input url")
        else:
            try:
                dispatchers = requests.get("{}/v1/dispatchers".format(const.centrum)).json()
                for dispatcher in dispatchers:
                    try:
                        parsed = furl(dispatcher)
                        temp = Dispatcher(parsed.username, parsed.host, parsed.port)
                        client = self.__connect(temp)
                        self.__dispatcher = temp
                        self.__client = client
                        break
                    except:
                        pass
                if self.__dispatcher is None:
                    raise Exception("no dispatchers available")
            except Exception:
                raise Exception("Unable to connect to centrum")                
    def __connect(self, dispatcher: Dispatcher) -> hprose.HproseHttpClient:
        return hprose.HttpClient("http://{}:{}/rpc".format(dispatcher.getIP(), dispatcher.getPort()))
    def getDispatcher(self) -> Dispatcher:
        return self.__dispatcher
    def __readTask(self, fn: str) -> str:
        f = open(fn, "r+")
        content = f.read()
        f.close()
        return content
    def Version(self) -> dict:
        return json.loads(self.__client.Version())
    def PeerCount(self) -> int:    
        return self.__client.PeerCount()
    def BlockByHash(self, hash: str) -> dict: 
        return json.loads(self.__client.BlockByHash(hash))
    def BlockByHeight(self, height: int) -> dict:
        return json.loads(self.__client.BlockByHeight(height))
    def Latest15Blocks(self) -> list:
        return json.loads(self.__client.Latest15Blocks())
    def LatestBlock(self) -> dict:
        return json.loads(self.__client.LatestBlock())
    def PendingCount(self) -> int: 
        return self.__client.PendingCount()
    def Score(self) -> float:
        return self.__client.Score()
    def Peers(self) -> list:
        return self.__client.Peers()
    def PublicKey(self) -> str:
        return self.__client.PublicKey()
    def NewJob(self, fn: str, name: str, priv: bool, privKey: str) -> str:
        return self.__client.NewJob(self.__readTask(fn), name, priv, privKey)
        
