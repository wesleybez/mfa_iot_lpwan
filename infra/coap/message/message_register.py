import json

class CoapMessageRegister():
    def __init__(self):
        number = 0
        message = ""
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toCSV(self):
        #todo trocar
        return self.login+","+self.password
    def fromCSV(self,payload):
        #todo trocar
        a = payload.split(",")
        self.login = a[0]
        self.password = a[1]