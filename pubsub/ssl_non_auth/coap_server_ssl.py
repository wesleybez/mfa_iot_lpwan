#https://github.com/Tanganelli/CoAPthon
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from resources.teste_resource import TesteResource
from resources.basic_resource import BasicResource
# Dtls
import ssl
import dtls
from dtls import do_patch
from dtls.wrapper import wrap_server, wrap_client

#
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
#######################
## observacao: rodar com 2.7 devido a compatibilidade do dtls
#######################
import socket

#TODO organizar
dir_seg="/home/wesley/backup_windows/backup_lenovo/"\
    +"documentos/documentos/educacao/pgcc_2018/201902/redes_westphall/"\
    +"artigo_protocolos_mensagem/docker/openwrt/mqtt/"
    
caminho_server_cert= dir_seg+"server_public.pem"
caminho_ca_cert= dir_seg+"ca_public.pem"
caminho_serv_key=dir_seg+"server_private.pem"

#server_cert = open("server.crt").read()
#server_key = open("server_private.pem").read()
#ca_cert = open("ca_public.pem").read()
cert_chain = open("seg/server_chain.pem").read()

host_address = ("127.17.0.1", 5683)

class TesteCoapServer():
    def __init__(self, host, port):
        #print("server_key:"+pem_server_key)
        #print("ca_cert   :"+pem_server_key)
        #logger.debug("cert_chain   :"+cert_chain)
        #inicializacao do DTLS
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #
        do_patch()
        self.sock = wrap_server(
            sock=self.sock, 
            keyfile=caminho_serv_key,#pem_server_key, 
            certfile=caminho_server_cert,#pem_server_key)#,
            ca_certs=caminho_ca_cert,#,
            ciphers="ECDHE+AESGCM")#pem_server_key)
             
            #cert_reqs, 
            #ssl_version, 
            
            #, 
            
            #do_handshake_on_connect, 
            #suppress_ragged_eofs, 
            #ciphers, 
            #curves, 
            #sigalgs, 
            #user_mtu, 
            #server_key_exchange_curve, 
            #server_cert_options
        
        logger.debug("inicializou socket ssl")
        
        #self.sock.bind((host,port))
        self.sock.bind(host_address)
        self.sock.listen(0)
        logger.debug("fez o bind")
        
        self.server = CoAP(
            (host,port),  
            starting_mid=None, 
            sock=self.sock
        )
        logger.debug("instanciou servidor")
        #CoAP.__init__(self, (host, port))
        self.server.add_resource('basic/', BasicResource())
        self.server.add_resource('teste', TesteResource())
        self.server.add_resource('sala/teste', TesteResource())
        self.server.add_resource('jardim/teste', TesteResource())
        logger.debug("adicionou recursos")
def main():
    server = TesteCoapServer("127.17.0.1", 5683)
    try:
        logger.debug("waiting for connection...")
        #server.listen(10)
    except KeyboardInterrupt:
        logger.debug ("Server Shutdown")
        server.close()
        logger.debug ("Exiting...")

if __name__ == '__main__':
    main()