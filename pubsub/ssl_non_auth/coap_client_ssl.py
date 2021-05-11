import ssl
from dtls.wrapper import wrap_server, wrap_client
from dtls import do_patch
import dtls

import requests

#Coapthon
#https://github.com/Tanganelli/CoAPthon
from coapthon import defines
from coapthon.client.helperclient import HelperClient
from coapthon.server.coap import CoAP as CoAPServer

from coapthon.messages.option import Option
from coapthon.messages.request import Request
from coapthon.messages.response import Response
#sistema operacional
import socket
import random
import threading
import unittest
import time
import tempfile
import os
from array import array

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

dir_base = "/home/wesley/backup_windows/backup_lenovo/documentos/"\
    +"documentos/educacao/pgcc_2018/201902/redes_westphall/"\
    +"artigo_protocolos_mensagem/docker/openwrt/mqtt/"
caminho_server_cert=dir_base + "server_public.pem"


def cb_put(response):
    logger.debug("dentro callback put")
    logger.debug(response)

def cb_get(response):
    logger.debug("dentro callback get")
    logger.debug(response)
    
def cb_delete(response):
    logger.debug("dentro callback delete")
    logger.debug(response)

def cb_request(response):
    logger.debug("dentro callback request")
    logger.debug(response)

try:
    # Set up a client side DTLS socket
    _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    do_patch()
    _sock = wrap_client(_sock,
       cert_reqs=ssl.CERT_REQUIRED,
       ca_certs=caminho_server_cert,
       ciphers="ECDHE+AESGCM",
       do_handshake_on_connect=False,user_mtu=1200)

    logger.debug(_sock)

    # Connect the CoAP client to the newly created socket
    server=("127.17.0.1", 5683)
    client = HelperClient(server, sock=_sock)
    logger.debug(client)
    # Do the communication
    
    #todo: iniciar conexao com ssl
    logger.debug("enviando: TESTE")
    #received_message = client.send_request("teste",cb_request, 10)
    client.put("basic/", "aleatorio_", cb_put, 10)
    #logger.debug("recebendo!")

    
    time.sleep(15)
    client.stop()
except requests.exceptions.RequestException as err:
    print(err, url)