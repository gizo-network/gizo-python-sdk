import pytest
import sys, os, base64
from robber import expect
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from gizo.gizo import Gizo
from gizo.utils import to_bytes, to_hex
from gizo.env import Env, Envs
import gizo.priorities as priorities

test = Gizo()

class TestGizo(object):
    def test_node(self):
        expect(test.Version()).to.contain("Version", "Height", "Blocks")
        expect(test.PeerCount()).to.be.an.integer()
        expect(test.Score()).to.be.a.float()
        expect(test.Peers()).to.be.a.list()
        expect(test.PublicKey()).to.be.a.string()
        expect(test.WorkersCount()).to.be.an.integer()
        expect(test.WorkersCountBusy()).to.be.an.integer()
        expect(test.WorkersCountNotBusy()).to.be.an.integer()
        expect(test.JobQueueCount()).to.be.an.integer()
    def test_job(self):
        expect(test.NewJob("../tmp/test.anko", "Factorial", False)).to.be.a.string()
        expect(test.NewExec(["test", "test"], 0, priorities.NORMAL, 0, 0, 0, 0, Envs(Env("test", "test")))).to.contain("Args", "Envs")
    def test_block(self):
        block = test.BlockByHeight(0)
        expect(block).to.contain("Header")
        expect(test.BlockByHash(to_hex(base64.b64decode(block["Header"]["Hash"])))['Height']) == block['Height'] #! json encodes byte arrays to base64 so to use the hash value we have to decode then convert to hex
        expect(test.LatestBlockHeight()).to.be.an.integer()
        expect(test.Latest15Blocks()).to.be.a.list()
        expect(test.BlockHashesHex()).to.be.a.list()
        expect(test.LatestBlock()).to.be.a.dict()
        expect(test.KeyPair()).to.be.a.dict()
    