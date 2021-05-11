import json

class CoapMessageAuth ( ):
    def __init__(self, message, session_id):
        self.message = message
        self.session_id = session_id
       
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)