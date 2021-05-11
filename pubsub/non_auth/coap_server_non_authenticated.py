#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from resources.teste_resource import TesteResource
import configparser
from resources.basic_resource import BasicResource

import logging

config = configparser.ConfigParser()
config.read('../config.ini')
LOOP_NUMBER = config.getint('geral','instance_number')
FATOR_MULT = config.getint('geral','mult_factor')
HOST = config.get('geral','host')
PORT = config.getint('geral','port')

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('basic/', BasicResource())
        self.add_resource('teste', TesteResource())
        self.add_resource('sala/teste', TesteResource())
        self.add_resource('jardim/teste', TesteResource())

def main():
    server = CoAPServer("127.17.0.1", 5683)
    try:
        print("waiting for connection...")
        server.listen(10)
    except KeyboardInterrupt:
        print ("Server Shutdown")
        server.close()
        print ("Exiting...")

if __name__ == '__main__':
    main()