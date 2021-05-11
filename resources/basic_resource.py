#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BasicResource(Resource):
    def __init__(self, name="BasicResource", coap_server=None):
        super(BasicResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = "Basic Resource"

    def render_GET(self, request):
        logger.debug("entrou no render_GET")
        self.payload = "{temperatura:30, {nome:abc, idade:33}}"
        return self

    def render_PUT(self, request):
        logger.debug("entrou no render_PUT")
        self.payload = request.payload
        return self

    def render_POST(self, request):
        logger.debug("entrou no render_POST")
        res = BasicResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        return res

    def render_DELETE(self, request):
        logger.debug("entrou no render_DELETE")
        return True
