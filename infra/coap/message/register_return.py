import json
from util.json_adapter import JsonAdapter

class RegisterReturn():
    def __init__(self, user, passwd, timestamp):
        self.user = user
        self.passwd = passwd
        self.timestamp = timestamp
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)#,sort_keys=True, indent=4)
    def fromJSON(self,payload):
        a = JsonAdapter.convertToDict(payload)
        self.passwd = a["passwd"]
        self.timestamp = a["timestamp"]
        self.user = a["user"]    