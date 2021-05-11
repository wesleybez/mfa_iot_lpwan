#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource


import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class TesteResource(Resource):
    def __init__(self, name="TesteResource", coap_server=None):
        super(TesteResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = "Teste Resource"

    def render_GET(self, request):
        return self

    def render_PUT(self, request):
        self.payload = request.payload
        logger.debug ("payload:",self.payload)
        return self

    def render_POST(self, request):
        res = TesteResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        return True
