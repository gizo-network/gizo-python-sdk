import requests
from furl import furl
import hprose
import base64
import json
import datetime
from os import path
from gizo.gizo import Gizo
from gizo.env import Env, Envs
import gizo.priorities as priorities
import gizo.utlis as helpers
# from gizo.gizo import Gizo, Env

# temp = Gizo()
# print(temp.WorkersCountNotBusy())
# print(temp.NewExec(["test", "test"], 0, priorities.NORMAL, 0, 0, 0, 0, Envs(Env("test", "test"))))

list = [116, 101, 115, 116, 105, 110, 103]
print(helpers.to_hex(list))
print(helpers.to_bytes(helpers.to_hex(list)))