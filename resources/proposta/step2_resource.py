# -*- coding: utf-8 -*-
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

#banco de dados
import sqlite3 

import logging
from db.db_register import DBRegister
from infra.coap.query_helper import QueryHelper
from infra.coap.message.factor_one_return import FactorOneReturn
from infra.coap.factor_two_entry import FactorTwoEntry
from infra.coap import device
from infra.coap.device import CoapDevice
from util.json_adapter import JsonAdapter
from infra.coap.auth_workflow_entry import AuthWorkFlowEntry
from infra.coap.message.factor_two_return import FactorTwoReturn
from resources.proposta.auth_inspector_resource import AuthInspectorResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class Step2PropostaResource(Resource):
    step2_queries = dict()
    
    def __init__(self, name="Advanced"):
        super(Step2PropostaResource, self).__init__(
            name, 
            coap_server=None, 
            visible=True, 
            observable=False, 
            allow_children=False)
        self.payload = "Step2 Resource"

    def render_GET_advanced(self, request, response):
        logger.debug("entrou no get login")           
        self.payload = request.payload
        return self, response


    def render_POST_advanced(self, request, response):
        self.payload = request.payload
        logger.debug("entrou no post advanced")
        print("payload:",request.payload)
        data = request.payload        
        #todo passar para json
        a = JsonAdapter.convertToDict(data)
        print("a:",a)
        
        return self.process_step2(request, response)
        
    def render_PUT_advanced(self, request, response):
        
        self.payload = request.payload
        user = request.payload        


        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response
    
    def process_step2(self,request, response):
        logger.debug("entrou no process step2")        

        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        
        response.content_type = defines.Content_types["application/json"]
        response.mid = request.mid
        defines.acknowledged = True         
        #inicio autenticacao
        
        a = JsonAdapter.convertToDict(request.payload)
        
        print(a)
        #busca pelo auth_code        
        entry = Step2PropostaResource.step2_queries[a["auth_code"]]
        
        result = "-1"
        
        if (entry != None) and (entry.query_result == a["query_response"]):
            print("resposta válida a query")
            result = "ok"
            #todo: passar para enum
            authEntry = AuthWorkFlowEntry(a["auth_code"],"authenticated",0)
            AuthInspectorResource.auth_workflow[a["auth_code"]]=authEntry
            
        print(AuthInspectorResource.auth_workflow)
        
        response.payload = FactorTwoReturn(result).toJSON()
        
        return self, response
