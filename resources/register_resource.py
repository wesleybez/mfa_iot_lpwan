#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines

from coapthon.messages import response
from coapthon.messages.response import Response
from coapthon.messages.request import Request

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RegisterResource(Resource):
    def __init__(self, name="RegisterResource", coap_server=None):
        #nao deixar visivel
        super(RegisterResource, self).__init__(name, 
            coap_server, 
            visible=True,
            observable=True, 
            allow_children=True
        )
        self.payload = "Register Resource"

    def render_GET(self, request):
        #enviar mensagem padrao de funcionando
        self.payload = request.payload
        logger.debug ("\ndentro do get ",self.payload)
        
        return self

    def render_PUT(self, request):
        #registra dispositivo na memoria/BD
        self.payload = request.payload
        logger.debug ("\ndentro do put ",self.payload)
        return self

    def render_POST_advanced(self, request, response):
        logger.debug("entrou no post advanced login")
        self.payload = request.payload
        par = Request()        
        device = request.payload
        adevice = device.split(",")
        
        for d in adevice:
            logger.debug("dados:",d)
        
        
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through POST :"+device
        response.code = defines.Codes.CREATED.number
        
        
        return self, response

    def render_DELETE(self, request):
        return True