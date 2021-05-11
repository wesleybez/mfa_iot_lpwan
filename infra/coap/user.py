import json

class CoapUser ( ):
    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toCSV(self):
        return "login="+self.login+", password="+self.password
    @staticmethod
    def fromCSV(payload):
        result = CoapUser()
        a = payload.split(",")
        result.login = a[0].split("=")[1]
        result.password = a[1].split("=")[1]
        return result
