import json
from builtins import staticmethod
from util.json_adapter import JsonAdapter

class CoapDevice ( ):
    
    def __init__(self, uuid=None, modelo=None, fabricante=None, nro_serie=None):
        self.uuid = uuid
        self.modelo = modelo
        self.fabricante = fabricante
        self.nro_serie = nro_serie
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def toCSV(self):
        return self.uuid+","+self.modelo+","+self.fabricante+","+self.nro_serie
    @staticmethod
    def fromCSV(payload):
        result = CoapDevice()
        a = payload.split(",")
        result.uuid = a[0]
        result.modelo = a[1]
        result.fabricante = a[2]
        result.nro_serie = a[3]
        return  result
    @staticmethod
    def fromJSON(payload):
        a = JsonAdapter.convertToDict(payload)
        result = CoapDevice()
        result.uuid = a["uuid"]
        result.modelo = a["modelo"]
        result.fabricante = a["fabricante"]
        result.nro_serie = a["nro_serie"]
        return result