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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class AuthInspectorResource(Resource):
    auth_workflow = dict()
    
    def __init__(self, name="Advanced"):
        super(AuthInspectorResource, self).__init__(
            name, 
            coap_server=None, 
            visible=True, 
            observable=False, 
            allow_children=False)
        self.payload = "AuthInspector Resource"

    def render_GET_advanced(self, request, response):
        logger.debug("entrou no get login")           
        self.payload = request.payload
        return self, response


    def render_POST_advanced(self, request, response):
        self.payload = request.payload
        logger.debug("entrou no post advanced")
        
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response
    
    @staticmethod
    def remove(hash_code):
        #verificar funcionamento
        AuthInspectorResource.auth_workflow.remove(hash_code)
    @staticmethod
    def get(hash_code):
        result = -1
        for e in AuthInspectorResource.auth_workflow :
            print(e)
            if (e["hash_code"]==int(hash_code)):
                result = e
        return result
    @staticmethod
    def saveToFile(filename):
        pickle.dump( AuthInspectorResource.auth_workflow, open( filename, "wb" ) )
        print("inicio salvando dados AuthWorkflow")
        for x in DBRegister.db :
            print(x)
        print("fim salvando dados AuthWorkflow")
    @staticmethod
    def loadFromFile(filename):
        AuthInspectorResource.auth_workflow = pickle.load( open( filename, "rb" ) )
        print("inicio lendo dados AuthWorkflow")
        for x in DBRegister.db :
            print(x)
        print("fim lendo dados AuthWorkflow")
        