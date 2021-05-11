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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class LoginResource(Resource):
    
    def __init__(self, name="Advanced"):
        super(LoginResource, self).__init__(name, coap_server=None, visible=True, observable=False, allow_children=False)
        self.payload = "Login Resource"
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
        #inicio autenticacao
        auser = user.split(",")        
        #primeiro passo, verificar login/senha
        # - inicialmente fixo
        
        #conectar e consultar usuario
        conn = sqlite3.connect("../../db/proposta1")
        
        
        cur = conn.execute("SELECT * FROM tb_login WHERE login='"+auser[0]+"' AND passwd='"+auser[1]+"'")
        logger.debug("sql","SELECT * FROM tb_login WHERE login='"+auser[0]+"' AND passwd='"+auser[1]+"'")
        if(cur.fetchone()==None) :
            logger.debug("não achou nada na consulta do sqlite3")
        
        if auser[0]=="sensor1" and auser[1]=="senha1" :
            resultado = ""+time.strftime('%Y%m%d%H%M%S')
            self.auth_codes.append(resultado)
            logger.debug("autenticado")
            
        else:
            resultado = "authentication_code:-1"
            logger.debug("nao autenticado")
            #response.code = "403"#defines.Codes.FORBIDDEN
        #fim autenticacao
        logger.debug(resultado)
        
        logger.debug("codigos de autenticacao ativos:")
        for x in self.auth_codes :
            logger.debug(x)
        
        response.payload = resultado
        logger.debug("response:",response)
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
        
        #conectar e consultar usuario
        conn = sqlite3.connect("../../db/proposta1")
        cur = conn.execute("SELECT * FROM tb_login WHERE login='"+auser[0]+"' AND passwd='"+auser[1]+"'")
        logger.debug("sql","SELECT * FROM tb_login WHERE login='"+auser[0]+"' AND passwd='"+auser[1]+"'")
        if(cur.fetchone()==None) :
            logger.debug("não achou nada na consulta do sqlite3")
        
        if auser[0]=="sensor1" and auser[1]=="senha1" :
            resultado = ""+time.strftime('%Y%m%d%H%M%S')
            self.auth_codes.append(resultado)
            logger.debug("autenticado")
            
        else:
            resultado = "authentication_code:-1"
            logger.debug("nao autenticado")
            #response.code = "403"#defines.Codes.FORBIDDEN
        #fim autenticacao
        logger.debug (resultado)
        response.payload = resultado
        
        logger.debug("codigos de autenticacao ativos:")
        for x in self.auth_codes :
            logger.debug(x)
        
        logger.debug("request:",request)
        logger.debug("response:",response)

        return self#, response

    def render_PUT_advanced(self, request, response):
        
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
        
        #conectar e consultar usuario
        conn = sqlite3.connect("../../db/proposta1")
        cur = conn.execute("SELECT * FROM tb_login WHERE login='"+auser[0]+"' AND passwd='"+auser[1]+"'")
        logger.debug("sql","SELECT * FROM tb_login WHERE login='"+auser[0]+"' AND passwd='"+auser[1]+"'")
        if(cur.fetchone()==None) :
            logger.debug("não achou nada na consulta do sqlite3")
        
        if auser[0]=="sensor1" and auser[1]=="senha1" :
            resultado = ""+time.strftime('%Y%m%d%H%M%S')
            logger.debug("autenticado")
            
        else:
            resultado = "authentication_code:-1"
            logger.debug("nao autenticado")
            #response.code = "403"#defines.Codes.FORBIDDEN
        #fim autenticacao
        logger.debug (resultado)
        response.payload = resultado
        logger.debug("response:",response)
        return self, response

    def render_DELETE_advanced(self, request, response):
        response.payload = "Response deleted"
        response.code = defines.Codes.DELETED.number
        return True, response