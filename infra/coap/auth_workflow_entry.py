import json
from util.json_adapter import JsonAdapter
from builtins import staticmethod

class AuthWorkFlowEntry():
    def __init__(self, auth_code, level, reputation):
        self.auth_code = auth_code
        self.level = level
        self.reputation = reputation

    def __str__(self):
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)#,sort_keys=True, indent=4)
    @staticmethod
    def fromJSON(payload):
        a = JsonAdapter.convertToDict(payload)
        result = AuthWorkFlowEntry()
        result.auth_code = a["auth_code"]
        result.level = a["level"]
        result.reputation = a["reputation"]
        return result