import requests
from furl import furl
import hprose
from gizo.gizo import Gizo

temp = Gizo()
print(temp.readTaskFile("./temp.anko"))