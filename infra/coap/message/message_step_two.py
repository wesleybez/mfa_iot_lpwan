import json

class CoapMessageStepTwo ( ):
    def __init__(self, query_response, auth_code):
        self.query_response = query_response    
        self.auth_code = auth_code    
       
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)