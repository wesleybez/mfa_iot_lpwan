import pickle

class DBRegister():
    db = []
    
    def __init__(self):
        self.db = []
    @staticmethod
    def add(hash_code,user, passwd, timestamp, register_data):
        entry = {"hash_code":hash_code,
                 "user":user,
                 "passwd":passwd,
                 "timestamp":timestamp,
                 "register_data":register_data}
        DBRegister.db.append(entry)
    @staticmethod
    def remove(hash_code):
        #verificar funcionamento
        DBRegister.db.remove(hash_code)
    @staticmethod
    def get(hash_code):
        result = -1
        for e in DBRegister.db :
            if (e["hash_code"]==hash_code):
                result = e
        return result
    @staticmethod
    def getByUser(user):
        result = -1
        for e in DBRegister.db :
            if (e["user"]==user):
                result = e
        return result
    @staticmethod
    def saveToFile(filename):
        pickle.dump( DBRegister.db, open( filename, "wb" ) )
        print("inicio salvando dados DBRegister")
        for x in DBRegister.db :
            print(x)
        print("fim salvando dados DBRegister")
    @staticmethod
    def loadFromFile(filename):
        DBRegister.db = pickle.load( open( filename, "rb" ) )
        print("inicio lendo dados DBRegister")
        for x in DBRegister.db :
            print(x)
        print("fim lendo dados DBRegister")
        
                