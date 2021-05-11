#https://github.com/Tanganelli/CoAPthon
from coapthon.client.helperclient import HelperClient
import threading
import time
import sys
import logging

#from guppy import hpy
import configparser
import json
from infra.coap.user import CoapUser
from infra.coap import mem_util


medicoes = open("/home/wesley/"+time.strftime('%Y%m%d')+"_coap_publish_non_auth.csv","w")
memoria = open("/home/wesley/"+time.strftime('%Y%m%d')+"_coap_memory_non_auth.csv","w")

config = configparser.ConfigParser()
config.read('../config.ini')
LOOP_NUMBER = config.getint('geral','instance_number')
FATOR_MULT = config.getint('geral','mult_factor')
HOST = config.get('geral','host')
PORT = config.getint('geral','port')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

path1 ="basic"
path2 ="sala/teste"
path3 ="jardim/teste"

def cb_put(response):
    i = 1
    #print("callback do put chamado")


def worker(cont):
#    h = hpy()
#    print h.heap()
    
    t_inicio = time.perf_counter()
    mem_inic = mem_util.getCurrentMemoryUsage()
    #mqtt client
    client = HelperClient(server=("127.0.0.1", PORT))    
    #client = mqtt.Client(protocol=mqtt.MQTTv31)
    t_connection = time.perf_counter()

    td_connection = t_connection - t_inicio 
    client.put("teste", "aleatorio_"+str(cont), cb_put, 10)    

    t_publish = time.perf_counter() 
    td_publish = t_publish - t_connection
    #

    t_subscribe = time.perf_counter()
    td_subscribe = t_subscribe - t_publish
    
    client.stop()
    
    t_disconnect = time.perf_counter()
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