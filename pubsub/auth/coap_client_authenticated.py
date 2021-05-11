#https://github.com/Tanganelli/CoAPthon
from coapthon.client.helperclient import HelperClient
import threading
import time
import logging
import configparser

import json

from infra.coap.user import CoapUser
from infra.coap.device import CoapDevice
from coapthon.messages.response import Response

from infra.coap import mem_util

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

medicoes = open("/home/wesley/"+time.strftime('%Y%m%d')+"_coap_publish_autenticated.csv","w")
memoria = open("/home/wesley/"+time.strftime('%Y%m%d')+"_coap_memory_autenticated.csv","w")

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('../config.ini')
LOOP_NUMBER = config.getint('geral','instance_number')
FATOR_MULT = config.getint('geral','mult_factor')
HOST = config.get('geral','host')
PORT = config.getint('geral','port')

path1 ="basic"
path2 ="sala/teste"
path3 ="jardim/teste"

client = None

auth_code = ""

def cb_get(response):
    logger.debug ("dentro do callback do get")
    #print(response)
    #client.stop
def cb_post_register(response):
    logger.debug ("dentro do callback do post do register")
    logger.debug(response)
def cb_post_login(response):
    logger.debug ("dentro do callback do post do login")
    logger.debug(response)
    auth_code = response.payload
    logger.debug("auth_code:",auth_code)
    #client.stop
def cb_put(response):
    logger.debug ("dentro do callback do put")
    #print(response)
    #response.stop()
    #client.stop
    
def registrar_dispositivo(client):
    #
    # conectar no servico de registro
    #
    logger.debug("Conectando no servico de registro")
    dispositivo = CoapDevice("001", "esp01", "NodeMcu", "00010001")
    response = client.post("register", dispositivo.toCSV(), cb_post_register, 1)
    if response is not None:
        logger.debug (response.pretty_print())
    logger.debug("registrado!")
    #client.stop()

def autenticar(client):
    #
    # conectar ao servico de autenticacao e obter credencial
    #
    #envio das credenciais
    logger.debug("Conectando no servico de autenticacao")
    usuario = CoapUser("sensor1","senha1")
    response = client.post("login", usuario.toCSV(), cb_post_login, 1)
    if response is not None:
        logger.debug (response.pretty_print())
    #client.stop()
    print("response",response)

def enviar_dados(client,cont):
    logger.debug("Conectando no servico de autenticacao")
    usuario = CoapUser("sensor1","senha1")
    client.put("teste", "aleatorio_"+str(cont), cb_put, 10)
    
def worker(cont):
    t_inicio = time.clock()
    mem_inic = mem_util.getCurrentMemoryUsage()
    #coap client
    client = HelperClient(server=("127.0.0.1", PORT))  
    autenticar(client)
    t_connection = time.clock()
    td_connection = t_connection - t_inicio
    
    enviar_dados(client, cont)     
   # client.put("teste", "aleatorio_"+str(cont), cb_put(), 10)    
    t_publish = time.clock()
    td_publish = t_publish - t_connection
    #
    #time.sleep(1000)
    #client.subscribe("casa/teste_2")
    #response = client.get(path2)
#    print response.pretty_print()
    #time.sleep(1000)
    t_subscribe = time.clock()
    td_subscribe = t_subscribe - t_publish
    #client.stop()
    t_disconnect = time.clock()
    td_disconnect = t_disconnect - t_subscribe
    mem_fim = mem_util.getCurrentMemoryUsage()
    
    medicoes.write(" "+str(cont+1)
                   +","+str(t_inicio*FATOR_MULT)
                   +","+str(td_connection*FATOR_MULT)
                   +","+str(td_publish*FATOR_MULT)
                   +","+str(td_subscribe*FATOR_MULT)
                   +","+str(td_disconnect*FATOR_MULT)
                   +"\n")
    medicoes.flush()
    memoria.write(" "+str(cont+1)
                  +","+str(mem_inic)
                  +","+str(mem_fim)
                  +","+str(mem_fim-mem_inic)+"\n")
    memoria.flush()
#medicoes.write("thread ,inicio ,conexao ,publicacao ,inscricao ,fim [x1000] \n")



clients = list()
for i in range(LOOP_NUMBER):
    c= threading.Thread(target=worker,args=(i,))
    clients.append(c)
    c.start()
    time.sleep(1)
        
time.sleep(5)

medicoes.close()
memoria.close()
#client.subscribe("casa/teste_2")