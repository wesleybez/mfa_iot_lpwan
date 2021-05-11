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
from resources.proposta.step2_resource import Step2PropostaResource
from resources.proposta.auth_inspector_resource import AuthInspectorResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class LoginPropostaResource(Resource):
    
    def __init__(self, name="Advanced"):
        super(LoginPropostaResource, self).__init__(
            name, 
            coap_server=None, 
            visible=True, 
            observable=False, 
            allow_children=False)
        self.payload = "Login Resource"
        
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
        
        return self.process_login(request, response)

    def render_PUT_advanced(self, request, response):
        
        self.payload = request.payload
        
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response
    
    def process_login(self,request, response):
        logger.debug("entrou no process login")
        user = request.payload        

        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        #response.payload = "Response changed through PUT"
        response.code = defines.Codes.CHANGED.number
        
        response.content_type = defines.Content_types["application/json"]
        response.mid = request.mid
        defines.acknowledged = True         
        #inicio autenticacao
        
        auser = JsonAdapter.convertToDict(user)        
        reg = DBRegister.getByUser(auser["login"])
        
        authenticated = False
        
        if reg != -1 :
            par_user = auser["login"]
            par_password = auser["password"]
            
            print("indice:",reg)
            print("request user:",par_user)
            print("request senha:",par_password)
            print("db user:",reg["user"])
            print("db senha:",reg["passwd"])
       
            if par_user==reg["user"] and par_password==reg["passwd"] :
                resultado = ""+time.strftime('%Y%m%d%H%M%S')                
                logger.debug("autenticado")
                authenticated = True
            else:
                resultado = "-1"
                logger.debug("senha errada")
        else:
            resultado = "-1"
            logger.debug("nao autenticado")
            logger.debug("nao achou usuario")
            #response.code = "403"#defines.Codes.FORBIDDEN
        #fim autenticacao
        
        query = "-1"
        if authenticated :
            #[0]-informacao
            #[1]-inicio
            #[2]-fim
            #[3]-inverter
            #[4]-rotacionar
            query = "1;0;2;1;1"
            
            device = CoapDevice.fromCSV(reg["register_data"])
            
            queryResponse = str(QueryHelper.processQuery(query, device.uuid),"utf-8")
            
            entry = FactorTwoEntry(resultado, queryResponse)
            Step2PropostaResource.step2_queries[resultado]=entry
            authEntry = AuthWorkFlowEntry(resultado,"compatibility",0)
            AuthInspectorResource.auth_workflow[resultado]=authEntry
        
        retorno = FactorOneReturn(resultado, query).toJSON()
        
        #aqui calcula o 
        
        
        logger.debug (retorno)
        response.payload = retorno
        
        logger.debug("codigos de autenticacao ativos:")
        print(Step2PropostaResource.step2_queries)
        logger.debug("niveis de autenticacao e reputacao:")
        print(AuthInspectorResource.auth_workflow)
        
        print("request:",request)
        print("response:",response)

        return self, response
    
