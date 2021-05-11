#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
import time

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AuthenticationResource(Resource):
    def __init__(self, name="AuthenticationResource", coap_server=None):
        super(AuthenticationResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = "Authentication Resource"

    def render_GET(self, request):
        self.payload = "{temperatura:30, {nome:abc, idade:33}}"+time.strftime('%Y%m%d')
        logger.debug("entrou get")
        return self

    def render_PUT(self, request):
        logger.debug("entrou get")
        logger.debug ("\n requisicao recebida")
        logger.debug ("\n payload:", request.payload)
        self.payload = request.payload
        return self

    def render_POST(self, request):
        logger.debug("entrou post")
        res = AuthenticationResource()
        
        user = request.payload
        #inicio autenticacao
        auser = user.split(",")        
        #primeiro passo, verificar login/senha
        # - inicialmente fixo
        if auser[0]=="sensor1" and auser[1]=="senha1" :
            resultado = "authentication_code:"+time.strftime('%Y%m%d%H%M%S')
            logger.debug ("\nautenticado")
            
        else:
            resultado = "authentication_code:-1"
            logger.debug ("\nnao autenticado")
            #res.code = defines.Codes.FORBIDDEN
        #fim autenticacao
        res.payload = resultado
        res.location_query = request.uri_query
        #res.payload = request.payload
        
        return res

    def render_DELETE(self, request):
        return True
