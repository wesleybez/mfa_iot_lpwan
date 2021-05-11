# -*- coding: utf-8 -*-
#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from resources.teste_resource import TesteResource
from resources.basic_resource import BasicResource

import logging
from resources.proposta.login_proposta_resource import LoginPropostaResource
from resources.proposta.register_proposta_resource import RegisterPropostaResource
from db.db_register import DBRegister
from resources.proposta.basic_proposta_resource import BasicPropostaResource
from resources.proposta.step2_resource import Step2PropostaResource
from resources.proposta.auth_inspector_resource import AuthInspectorResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('login/', LoginPropostaResource())
        self.add_resource('step2/', Step2PropostaResource())
        
        self.add_resource('authInspector/', AuthInspectorResource())
        
        self.add_resource('register/', RegisterPropostaResource())
        self.add_resource('basic/', BasicPropostaResource())
        self.add_resource('teste', TesteResource())
        self.add_resource('sala/teste', TesteResource())
        self.add_resource('jardim/teste', TesteResource())

def main():
    #inicializar dados
    try:
        DBRegister.loadFromFile("./registro.txt")
    except :
        print("arquivo não existente")
    #host_address = ("127.0.0.1", 5684)
    #server = CoAPServer("0.0.0.0", 5683)
    #observacao: precisar ser o endereco para não ficar retransmitindo
    server = CoAPServer("127.17.0.1", 5683)
    try:
        print("Servidor da Proposta com autenticacao em espera...")
        server.listen(10)
    except KeyboardInterrupt:
        print ("Server Shutdown")
        server.close()
        print ("Exiting...")

if __name__ == '__main__':
    main()