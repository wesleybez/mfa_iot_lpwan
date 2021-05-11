# -*- coding: utf-8 -*-
#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon import defines

from coapthon.messages import response
from coapthon.messages.response import Response
from coapthon.messages.request import Request

import logging
import hashlib
import time
from db.db_register import DBRegister
from infra.coap.message.register_return import RegisterReturn
from argcomplete import debug

from coapthon.messages.response import Response

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
    
class RegisterPropostaResource(Resource):
    db = DBRegister()
    
    def __init__(self, name="RegisterPropostaResource", coap_server=None):
        #nao deixar visivel
        super(RegisterPropostaResource, self).__init__(name, 
            coap_server, 
            visible=True,
            observable=False, 
            allow_children=True
        )
        self.payload = "Register Resource"

    #def render_GET(self, request):
    def render_GET_advanced(self, request, response):
        #enviar mensagem padrao de funcionando
        self.payload = request.payload
        logger.debug ("\ndentro do get ")#,self.payload)        
        
        request.parame
        
        assert(isinstance(response, Response))
        response.mid = request.mid
        defines.acknowledged = True
        
        caminhos = request.uri_path.split("/")
        if caminhos[1]=="save" :
            DBRegister.saveToFile("./registro.txt")
            response.payload = "dados salvos"
            self.payload = "dados salvos"
            response.code = defines.Codes.CREATED.number#CREATED.number
            print("dentro do save")
        elif caminhos[1]=="load" :
            DBRegister.loadFromFile("./registro.txt")
            response.payload = "dados carregados"
            self.payload = "dados carregados"
            response.code = defines.Codes.CREATED.number#CREATED.number
            print("dentro do load")
        else :
            logger.debug("opcao invalida")
            response.code = defines.Codes.NOT_IMPLEMENTED.number#CREATED.number
        return self, response

    def render_PUT(self, request):
        #registra dispositivo na memoria/BD
        #self.payload = request.payload
        logger.debug ("\ndentro do put ")
        
        DBRegister.saveToFile("./registro.txt")
        response.payload = "dados salvos"
        self.payload = "dados salvos"
        response.code = defines.Codes.CREATED.number#CREATED.number
        print("dentro do save")
            
        return self

    def render_POST_advanced(self, request, response):
        logger.debug("entrou no post advanced login")
        self.payload = request.payload
        par = Request()        
        device = request.payload
        adevice = device.split(",")
        '''    
        print ("device   :",device)
        print ("adevice  :",adevice)
        print ("request  :",request)
        print ("uri_path :",request.uri_path)
        print ("senha    :", gerar_senha(device))
        print ("usuario  :", gerar_usuario(device))
        print ("timestamp:", time.strftime('%Y%m%d%H%M%S'))
        '''
        caminhos = request.uri_path.split("/")
        #logger.("caminhos :",caminhos)
        #url = urlparse(request.uri_path)
                
        """ for d in adevice:
            logger.debug("dados:",str(d))
        """
        hash_code = self.gerar_hash(device)
        register_response = self.device_register(hash_code,device)
        
        from coapthon.messages.response import Response
        assert(isinstance(response, Response))
        response.payload = ""+register_response
        self.payload = ""+register_response
        response.code = defines.Codes.CHANGED.number#CREATED.number
        response.mid = request.mid
        defines.acknowledged = True

        print("response.token:",response.token)
        print("request.token:",request.token)
        print("response.mid:",response.mid)
        print("request.mid:",request.mid)
        
        DBRegister.saveToFile("./registro.txt")
        #print("response:",response)
        
        return self, response


    def render_DELETE(self, request):
        logger.debug ("\ndentro do DELETE")
        DBRegister.loadFromFile("./registro.txt")
        response.payload = "dados carregados"
        self.payload = "dados carregados"
        response.code = defines.Codes.CREATED.number
        
        return True
    
    #verifica se o dispostivo ja foi registrado
    #  caso nao, o registra
    #  caso sim, volta -1
    def device_register (self, hash_code, device):
        result = "-1"
        i = DBRegister.get(hash_code)
        if ( i!=-1 ):
            logger.debug("ja registrado!")
        else :
            logger.debug("registrando...")
        
            usuario = self.gerar_usuario(device)
            senha = self.gerar_senha(device)
            timestamp = time.strftime('%Y%m%d%H%M%S')
        
            DBRegister.add(hash_code, 
                       usuario, 
                       senha, 
                       timestamp, 
                       device)
            
            result = RegisterReturn(usuario, senha, timestamp).toJSON()
        
        return result
        #calcula hash
    def gerar_hash(self,device):
            #gerar json e depois hash
        b_device = device.encode()
        md5 = hashlib.md5(b_device)
        #print("md5:",md5.hexdigest())
        return md5.hexdigest()
        
    def gerar_senha(self, device):
        #todo: gerar senha
        str_hash = self.gerar_hash(device)
        senha = str_hash[0:5]
        #print("senha:",senha)
        return senha

    def gerar_usuario(self, device):
        str_hash = self.gerar_hash(device)
        usuario = str_hash[5:10]
        #print("usuario:",usuario)
        return usuario
