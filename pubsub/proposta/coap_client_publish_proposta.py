#https://github.com/Tanganelli/CoAPthon
from coapthon.client.helperclient import HelperClient
import threading
import time
import logging
import configparser

import numpy as np
from numpy import random
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
import json

from infra.coap.user import CoapUser
from infra.coap.device import CoapDevice
from db.db_client_devices import DBClientDevices
from util.json_adapter import JsonAdapter
from infra.coap.query_helper import QueryHelper
from infra.coap.message.message_step_two import CoapMessageStepTwo
from infra.coap.message.message_data import CoapMessageData

medicoes = open("/home/wesley/"+time.strftime('%Y%m%d')+"_coap_publish_proposta.csv","w")

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

indice = 0
client = None

auth_code = ""

e = threading.Event()

def cb_put():
    i = 1
    
def cb_post_login(response):
    """ Callback do post de login.
     
        Processa a resposta do login e submete o segundo passo da autenticação multifator
    """
    global client
    global auth_code
    global e
    logger.debug("dentro do callback do post do passo1")
    logger.debug("response dentro do callback do post do passo1:",response)
    a = JsonAdapter.convertToDict(response.payload)
    print(a)
    query=a["query"]
    
    if(query!=1):
        auth_code = a["auth_code"]
        resultado = QueryHelper.processQuery(query, DBClientDevices.db[indice]["uuid"])
        logger.debug("dentro do callback do post do passo1 - resultado query:", resultado)        
        query_result= CoapMessageStepTwo(str(resultado,"utf-8"),a["auth_code"])
        #todo: consertar isso para funcionar com o mesmo client
        client2 = HelperClient(server=(HOST, PORT))
        client2.post("step2", query_result.toJSON(), cb_post_passo2, 10)
    else :
        print("dentro do callback do post do passo1 - sem segundo fator")
        logger.debug("sinalizando para thread continuar...")
        e.set()
    
def cb_post_passo2(response):
    """ Callback do post de step2.
     
        Processa a resposta do passo2
    """
    logger.debug("dentro do callback do post do passo2")
    logger.debug("response dentro do callback do post do passo2:",response)
    a = JsonAdapter.convertToDict(response.payload)
    logger.debug(a)
    logger.debug("sinalizando para thread continuar...")
    e.set()

def cb_post_publish(response):
    logger.debug("dentro do callback da publicacao")
    logger.debug("response dentro do callback da publicacao:",response)
    #a = JsonAdapter.convertToDict(response.payload)
    #print(a)

def worker(cont):
    global indice
    global client
    global e
    
    indice = cont
    
    t_inicio = time.perf_counter()
    #coap client
    client = HelperClient(server=(HOST, PORT))  
    #
    # conectar ao servico de autenticacao e obter credencial
    #
    #envio das credenciais
    print(cont)
    usuario = CoapUser(DBClientDevices.db[cont]["user"],
                       DBClientDevices.db[cont]["passwd"])
    #usuario = CoapUser("sensor1","senha1")
    client.post("login", usuario.toJSON(), cb_post_login, 10)
    
    #response = client.put("login", "sensor1;senha1", cb_put(), 10)
    t_connection = time.perf_counter()
    td_connection = t_connection - t_inicio 
   # client.put("teste", "aleatorio_"+str(cont), cb_put(), 10)    
    t_publish = time.perf_counter() 
    td_publish = t_publish - t_connection
    #
    #time.sleep(1000)
    """
        publica valores
    """
    #todo: esperar por um notify do callback ou finalizar
    logger.debug("esperando sinalizacao...")
    e.wait()    
    #todo: consertar para usar o mesmo cliente sempre
    client_publish = HelperClient(server=(HOST, PORT))
    #envios corretos
    for x in range(100) :        
        message_data = CoapMessageData(str(random.randint(10)), auth_code)    
        client_publish.post("basic", message_data.toJSON(), cb_post_publish, 10)
        time.sleep(1)
    #envio errado - medicao errada
    message_data = CoapMessageData(str(50+random.randint(30)), auth_code)    
    client_publish.post("basic", message_data.toJSON(), cb_post_publish, 10)
    time.sleep(1)
    
    #envio errado - auth code invalido
    message_data = CoapMessageData(str(50+random.randint(30)), "930192")    
    client_publish.post("basic", message_data.toJSON(), cb_post_publish, 10)
    time.sleep(1)

    #client.subscribe("casa/teste_2")
    #response = client.get(path2)
    #print response.pretty_print()
    #time.sleep(1000)
    t_subscribe = time.perf_counter() 
    td_subscribe = t_subscribe - t_publish
    #client.stop()
    t_disconnect = time.perf_counter()
    td_disconnect = t_disconnect - t_subscribe
    
    medicoes.write(" "+str(cont+1)
                   +","+str(t_inicio*FATOR_MULT)
                   +","+str(td_connection*FATOR_MULT)
                   +","+str(td_publish*FATOR_MULT)
                   +","+str(td_subscribe*FATOR_MULT)
                   +","+str(td_disconnect*FATOR_MULT)
                   +"\n")
    
#medicoes.write("thread ,inicio ,conexao ,publicacao ,inscricao ,fim [x1000] \n")
try:
    DBClientDevices.loadFromFile("./client_devices.txt")
except :
    print("arquivo não existente")

    
clients = list()
    
for i in range(LOOP_NUMBER):
    c= threading.Thread(target=worker,args=(i,))
    clients.append(c)
    c.start()
    time.sleep(1)        
time.sleep(15)
#client.subscribe("casa/teste_2")