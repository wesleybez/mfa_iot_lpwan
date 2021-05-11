import json
from util.json_adapter import JsonAdapter
class FactorOneReturn():
    def __init__(self, auth_code, query):
        self.auth_code = auth_code
        self.query = query        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)#,sort_keys=True, indent=4)
    def fromJSON(self,payload):
        a = JsonAdapter.convertToDict(payload)
        self.auth_code = a["auth_code"]
        self.query = a["query"]