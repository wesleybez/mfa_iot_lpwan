#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
import numpy as np

import logging
from util.json_adapter import JsonAdapter
from resources.proposta.auth_inspector_resource import AuthInspectorResource

#logging.basicConfig(filename='../../basic.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#logger.addHandler(ch)

class BasicPropostaResource(Resource):
    queue = []
    def __init__(self, name="BasicPropostaResource", coap_server=None):
        super(BasicPropostaResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = "Basic Resource"
        self.mean = 0.0
        self.dp = 0.0
        self.sum = 0
        
        

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
        res = BasicPropostaResource()
        res.location_query = request.uri_query
        res.payload = request.payload
        
        logger.debug("payload:",request.payload)
        a = JsonAdapter.convertToDict(request.payload)
        logger.debug("dict a:",a)
        
        if(a["auth_code"] in AuthInspectorResource.auth_workflow):
            logger.debug("codigo aceito")
            BasicPropostaResource.queue.append(a["data"])
        else:
            logger.error("codigo rejeitado - auth_code inexistente")
            return res
            
        logger.debug(BasicPropostaResource.queue)
        
        array = np.array(BasicPropostaResource.queue,dtype='i')
        
        self.mean = np.mean(array)
        self.dp   = np.std(array)
        diferenca = abs(float(
            str(
                self.mean.astype(float)))-int(a["data"]))
        gtStd = abs(float(
            str(self.mean.astype(float)))-int(a["data"])) > self.dp
        logger.debug("\n\nmean:", self.mean)
        logger.debug("std :", self.dp)  
        logger.debug("mean diff:", diferenca)
        logger.debug("gt std:", gtStd)
        if gtStd and len(BasicPropostaResource.queue)>50 :
            logger.error("greater than standard deviantion:")
            logger.error(a["data"])
            logger.error(self.dp)
            logger.error(self.mean)
            logger.error(a["auth_code"])
              
        
        return res

    def render_DELETE(self, request):
        logger.debug("entrou no render_DELETE")
        return True
