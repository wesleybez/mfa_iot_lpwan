import pickle

class DBClientDevices():
    db = []
    
    def __init__(self):
        self.db = []
    @staticmethod
    def add(hash_code,user, passwd, timestamp, device):
        entry = {"hash_code":hash_code,
                 "user":user,
                 "passwd":passwd,
                 "timestamp":timestamp,
                 "uuid":device.uuid,
                 "modelo":device.modelo,
                 "fabricante":device.fabricante,
                 "nro_serie":device.nro_serie}
        
        DBClientDevices.db.append(entry)
    @staticmethod
    def remove(hash_code):
        #verificar funcionamento
        DBClientDevices.db.remove(hash_code)
    @staticmethod
    def get(index):
        return DBClientDevices.db[index]
    @staticmethod
    def getHash(hash_code):
        result = -1
        for e in DBClientDevices.db :
            if (e["hash_code"]==hash_code):
                result = e
        return result
    @staticmethod
    def getByUser(user):
        result = -1
        for e in DBClientDevices.db :
            if (e["user"]==user):
                result = e
        return result
    @staticmethod
    def saveToFile(filename):
        pickle.dump( DBClientDevices.db, open( filename, "wb" ) )
        
        print("inicio salvando dados DBClientDevices")
        for x in DBClientDevices.db :
            print(x)
        print("fim salvando dados DBClientDevices")
    @staticmethod
    def loadFromFile(filename):
        DBClientDevices.db = pickle.load( open( filename, "rb" ) )
        print("inicio lendo dados DBClientDevices")
        for x in DBClientDevices.db :
            print(x)
        print("fim lendo dados DBClientDevices")
    