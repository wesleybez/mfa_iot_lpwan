import json
from util.json_adapter import JsonAdapter
from builtins import staticmethod

class FactorTwoEntry():
    def __init__(self, auth_code, query_result):
        self.auth_code = auth_code
        self.query_result = query_result
    def __str__(self):
        return self.toJSON()
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)#,sort_keys=True, indent=4)
    @staticmethod
    def fromJSON(payload):
        a = JsonAdapter.convertToDict(payload)
        result = FactorTwoEntry()
        result.auth_code = a["auth_code"]
        result.query_result = a["query_result"]
        return result