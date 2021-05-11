from builtins import staticmethod

class QueryHelper():
    @staticmethod
    def processQuery(query, info):
        q = query.split(";")
    
        begin = int(q[1])
        end = int(q[2])    
    
        isInverted = q[3]=="1"
        isRotated  = q[4]=="1"
    
        str = info[begin:end]
        result = str.encode()
    
        print("str      :",info,"begin    :",begin,"end      :",
              end,"inverted :",isInverted,"isRotated:",isRotated,
              "sliced   :",str,"bytes    :",result)
    
        if(isInverted):
            print("era para inverter")
            #iResult = int(result)
            #iResult = (iResult * -1) - 1            
            #result = str(iResult)
    
        if(isRotated) :
            print("era para rotacionar")
        
        return result
            