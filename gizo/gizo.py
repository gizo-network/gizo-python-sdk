import requests
import hprose
import json
import base64
import sys
from os import path
from furl import furl
from gizo.centrum import CENTRUM
from gizo.dispatcher import Dispatcher
from gizo.env import Envs
from gizo.job import JobRequest

class Gizo:
    def __init__(self, url: str =None, export_file: str= None):
        self.__dispatcher: Dispatcher = None
        self.__client: hprose.HproseHttpClient = None
        self.__file: str = None
        self.__keys: dict = None

        if export_file is None:
            self.__file = ".gizo"
        else:
            self.__file = export_file    
            
        if path.isfile(self.__file):
            try:
                self.__import_config()
                self.__client = self.__connect_dispatcher(self.__dispatcher)
            except Exception:
                self.__connect()
                self.__export_config()
        else:
            if url is not None:
                try:
                    self.__dispatcher = Dispatcher(url)
                    self.__client = self.__connect_dispatcher(self.__dispatcher)
                    self.__keys = self.KeyPair()
                    self.__export_config()
                except Exception as e:
                    print(str(e))
                    sys.exit(1)
            else:
                self.__connect()
                self.__keys = self.KeyPair()
                self.__export_config()
    def __import_config(self):
        f = open(self.__file, "r")
        content = json.loads(f.read())
        f.close()
        self.__dispatcher = Dispatcher(content["dispatcher"])
        self.__keys = content["keys"]
    def __export_config(self):
        temp: dict = {}
        temp["dispatcher"] = self.__dispatcher.url
        temp["keys"] = self.__keys
        f = open(self.__file, "w+")
        f.write(json.dumps(temp))
        f.close()
    def __connect(self):
        dispatchers = requests.get("{}/v1/dispatchers".format(CENTRUM)).json()
        for dispatcher in dispatchers:
            try:
                temp = Dispatcher(dispatcher)
                self.__client = self.__connect_dispatcher(temp)
                self.__dispatcher = temp                
                break
            except Exception:
                pass
        if self.__dispatcher is None:
            raise Exception("no dispatchers available")   
    def __connect_dispatcher(self, dispatcher: Dispatcher) -> hprose.HproseHttpClient:
        return hprose.HttpClient(dispatcher.rpc())
    def __readTask(self, fn: str) -> str:
        f = open(fn, "r")
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
    def NewJob(self, fn: str, name: str, priv: bool) -> str:
        return self.__client.NewJob(self.__readTask(fn), name, priv, self.__keys['priv'])
    def NewExec(self, args:list=None, retries: int=None, priority:int=None, backoff:int=None, exec_time: int=None, interval:int=None, ttl:int=None, envs:Envs=None) -> dict:
        return json.loads(self.__client.NewExec(args, retries, priority, backoff, exec_time, interval, ttl, self.__keys['pub'], json.dumps(envs.envs)))
    def WorkersCount(self) -> int:
        return self.__client.WorkersCount()
    def WorkersCountBusy(self) -> int:
        return self.__client.WorkersCountBusy()
    def WorkersCountNotBusy(self) -> int:
        return self.__client.WorkersCountNotBusy()
    def ExecStatus(self, job_id: str, exec_hash: list) -> str:
        return self.__client.ExecStatus(job_id, exec_hash)
    def CancelExec(self, exec_hash:list):
        return self.__client.CancelExec(exec_hash)
    def ExecTimestamp(self, job_id: str, exec_hash: list) -> int:
        return self.__client.ExecTimestamp(job_id, exec_hash)
    def ExecTimestampString(self, job_id: str, exec_hash: list) -> str:
        return self.__client.ExecTimestampString(job_id, exec_hash)
    def ExecDurationNanoseconds(self, job_id: str, exec_hash: list) -> int:
        return self.__client.ExecDurationNanoseconds(job_id, exec_hash)
    def ExecDurationSeconds(self, job_id: str, exec_hash: list) -> float:
        return self.__client.ExecDurationSeconds(job_id, exec_hash)
    def ExecDurationMinutes(self, job_id: str, exec_hash: list) -> float:
        return self.__client.ExecDurationMinutes(job_id, exec_hash)
    def ExecDurationString(self, job_id: str, exec_hash: list) -> str:
        return self.__client.ExecDurationString(job_id, exec_hash)
    def ExecArgs(self, job_id: str, exec_hash: list) -> list:
        return self.__client.ExecArgs(job_id, exec_hash)
    def ExecErr(self, job_id: str, exec_hash: list):
        return self.__client.ExecErr(job_id, exec_hash)
    def ExecPriority(self, job_id: str, exec_hash: list) -> int:
        return self.__client.ExecPriority(job_id, exec_hash)
    def ExecResult(self, job_id: str, exec_hash: list):
        return self.__client.ExecResult(job_id, exec_hash)
    def ExecRetries(self, job_id: str, exec_hash: list) -> int:
        return self.__client.ExecRetries(job_id, exec_hash)
    def ExecBackoff(self, job_id: str, exec_hash: list) -> float:
        return self.__client.ExecBackoff(job_id, exec_hash)
    def ExecExecutionTime(self, job_id: str, exec_hash: list) -> int:
        return self.__client.ExecExecutionTime(job_id, exec_hash)
    def ExecExecutionTimeString(self, job_id: str, exec_hash: list) -> str:
        return self.__client.ExecExecutionTimeString(job_id, exec_hash)
    def ExecInterval(self, job_id: str, exec_hash: list) -> int:
        return self.__client.ExecInterval(job_id, exec_hash)
    def ExecBy(self, job_id: str, exec_hash: list) -> str:
        return self.__client.ExecBy(job_id, exec_hash)
    def ExecTtlNanoseconds(self, job_id: str, exec_hash: list) -> int:
        return self.__client.ExecTtlNanoseconds(job_id, exec_hash)
    def ExecTtlSeconds(self, job_id: str, exec_hash: list) -> float:
        return self.__client.ExecTtlSeconds(job_id, exec_hash)
    def ExecTtlMinutes(self, job_id: str, exec_hash: list) -> float:
        return self.__client.ExecTtlMinutes(job_id, exec_hash)
    def ExecTtlHours(self, job_id: str, exec_hash: list) -> float:
        return self.__client.ExecTtlHours(job_id, exec_hash)
    def ExecTtlString(self, job_id: str, exec_hash: list) -> str:
        return self.__client.ExecTtlString(job_id, exec_hash)
    def JobQueueCount(self) -> int:
        return self.__client.JobQueueCount()
    def LatestBlockHeight(self) -> int:
        return self.__client.LatestBlockHeight()
    def Job(self, job_id: str) -> dict:
        return json.loads(self.__client.Job(job_id))
    def JobSubmisstionTimeUnix(self, job_id: str) -> int:
        return self.__client.JobSubmisstionTimeUnix(job_id)
    def JobSubmisstionTimeString(self, job_id: str) -> str:
        return self.__client.JobSubmisstionTimeString(job_id)
    def IsJobPrivate(self, job_id: str) -> bool:
        return self.__client.IsJobPrivate(job_id)
    def JobName(self, job_id: str) -> str:
        return self.__client.JobName(job_id)
    def JobLatestExec(self, job_id: str) -> dict:
        return json.loads(self.__client.JobLatestExec(job_id))
    def JobExecs(self, job_id: str) -> dict:
        return json.loads(self.__client.JobExecs(job_id))
    def BlockHashesHex(self) -> list:
        return self.__client.BlockHashesHex()
    def KeyPair(self) -> dict: 
        return json.loads(self.__client.KeyPair())
    def Solo(self, jr: JobRequest):
        return self.__client.Solo(jr.jr())
    def Chord(self, jrs: list, callback_jr: JobRequest):
        return self.__client.Chord(jrs, callback_jr)
    def Chain(self, jrs: list, callback_jr: JobRequest):
        return self.__client.Chain(jrs, callback_jr)
    def Batch(self, jrs: list, callback_jr: JobRequest):
        return self.__client.Batch(jrs, callback_jr)