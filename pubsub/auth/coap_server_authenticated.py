#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from resources.teste_resource import TesteResource
from resources.basic_resource import BasicResource
from resources.authentication.login_basic_resource import LoginBasicResource
from resources.register_resource import RegisterResource

import logging
from resources.auth_resource import AuthenticationResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('auth/', AuthenticationResource())
        self.add_resource('login/', LoginBasicResource())
        self.add_resource('basic/', BasicResource())
        self.add_resource('register/', RegisterResource())
        self.add_resource('sala/teste', TesteResource())
        self.add_resource('jardim/teste', TesteResource())

def main():
    server = CoAPServer("127.17.0.1", 5683)
    try:
        print("Servidor com autenticacao em espera...")
        server.listen(10)
    except KeyboardInterrupt:
        print ("Server Shutdown")
        server.close()
        print ("Exiting...")

if __name__ == '__main__':
    main()