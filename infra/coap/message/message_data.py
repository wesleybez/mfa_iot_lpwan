import json
class CoapMessageData():
    def __init__(self, data,auth_code=None):
        self.auth_code = auth_code
        self.data = data
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)