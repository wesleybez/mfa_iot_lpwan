from builtins import staticmethod
class JsonAdapter():
    def __init__(self, id):
        self.id = id
    @staticmethod
    def convertToDict(jsonStr):
        s1=jsonStr[1:(len(jsonStr)-1)]
        s1 = s1.strip()        
        campos = s1.split(",")        
        a = dict()
        for s in campos :
            l = s.strip().split(":")
            l[1]=l[1].strip()
            a[l[0][1:(len(l[0])-1)]]=l[1][1:(len(l[1])-1)]
        return a