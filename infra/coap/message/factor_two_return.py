import json
from util.json_adapter import JsonAdapter

class FactorTwoReturn():
    def __init__(self, result):        
        self.result = result
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)#,sort_keys=True, indent=4)
    def fromJSON(self,payload):
        a = JsonAdapter.convertToDict(payload)
        self.result = a["result"]
