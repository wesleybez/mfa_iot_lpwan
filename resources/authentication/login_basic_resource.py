# https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines

import json
from coapthon.messages import response
from coapthon.messages.response import Response
from coapthon.messages.request import Request
from datetime import date
import time
from _ast import In

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class LoginBasicResource(Resource):
    
    def __init__(self, name="Advanced"):
        super(LoginBasicResource, self).__init__(
            name,
            coap_server=None,
            visible=True, 
            observable=False, 
            allow_children=False)
        self.payload = "Login Basic Resource"
        self.auth_codes = []

    def render_GET_advanced(self, request, response):
        logger.debug("entrou no get login")
        
        self.payload = request.payload
        user = request.payload        

        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        response.mid = request.mid
        defines.acknowledged = True         
        #TODO
        return self, response


    def render_POST_advanced(self, request, response):
        self.payload = request.payload
        user = request.payload        

        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        response.mid = request.mid
        defines.acknowledged = True         
        #inicio autenticacao
        auser = user.split(",")        
        #primeiro passo, verificar login/senha
        # - inicialmente fixo
        
        if auser[0]=="sensor1" and auser[1]=="senha1" :
            resultado = ""+time.strftime('%Y%m%d%H%M%S')
            self.auth_codes.append(resultado)
            logger.debug("autenticado")
            
        else:
            resultado = "authentication_code:-1"
            logger.debug("nao autenticado")
            #response.code = "403"#defines.Codes.FORBIDDEN
        #fim autenticacao
        response.payload = resultado
        
        return self#, response

    def render_PUT_advanced(self, request, response):
        #TODO
        self.payload = request.payload
        user = request.payload        

        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        response.mid = request.mid
        defines.acknowledged = True         
        
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response