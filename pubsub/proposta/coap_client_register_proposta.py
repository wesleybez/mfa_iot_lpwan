#https://github.com/Tanganelli/CoAPthon
from coapthon.client.helperclient import HelperClient
import threading
import time
import logging
import configparser

import json

from infra.coap.user import CoapUser
from infra.coap.device import CoapDevice
from infra.coap.message.register_return import RegisterReturn
from db.db_client_devices import DBClientDevices
from util.json_adapter import JsonAdapter

medicoes = open("/home/wesley/"+time.strftime('%Y%m%d')+"_coap_register_proposta.csv","w")

#logging.basicConfig(level=logging.ERROR)
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

dispositivo = None

def cb_put_save(response):
    print("entrou no get do save")
    print(response)
    
def cb_delete_load(response):
    print("entrou no get do load")
    print(response)
    
def cb_put(response):
    logger.debug ("dentro do callback do put do register")
    logger.debug("response:",response)
    
def cb_post(response):
    logger.debug ("dentro do callback do post do register")
    #print("response:",response)
    #print("response.payload:",response.payload)
    
    #ja registrado
    if response.payload=="-1" :
        print("ja registrado")
        return None
    
    
    if response is not None:
        print (response.pretty_print())
        retorno = RegisterReturn("","","")
                
        a = JsonAdapter.convertToDict(response.payload)
        """
        s1=response.payload[1:(len(response.payload)-1)]
        s1 = s1.strip()
        print(s1)
        campos = s1.split(",")
        a = dict()
        for s in campos :
            #print(s)
            l = s.strip().split(":")
            l[1]=l[1].strip()
            a[l[0][1:(len(l[0])-1)]]=l[1][1:(len(l[1])-1)]
            #print(l[0])
            #print(l[1]) 
        
        #print(a)
        """
        #erro ao converter de json para object
        #retorno = retorno.fromJSON(response.payload)
        
        #print(retorno)
        #dispositivo vazio
        print(dispositivo)
        DBClientDevices.add("", a["user"], a["passwd"], a["timestamp"], dispositivo)
        
    #client.stop()
    
def worker(cont):
    global dispositivo
    dispositivo = CoapDevice("0"+str(cont), "esp01", "NodeMcu", "00010001"+str(cont))

    t_inicio = time.perf_counter()
    #coap client
    client = HelperClient(server=(HOST, PORT))  
    t_connection = time.perf_counter()
    td_connection = t_connection - t_inicio 

    #
    # conectar no servico de registro
    #
    response = client.post("register/", dispositivo.toCSV(), cb_post)   
    
    if response is not None:
        print (response.pretty_print())
        
    #print(response)
    #if response is not None:
    #    print (response.pretty_print())     
   # client.put("teste", "aleatorio_"+str(cont), cb_put(), 10)    
    t_publish = time.perf_counter() 
    td_publish = t_publish - t_connection
    #
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


#client = HelperClient(server=(HOST, PORT))
#response = client.delete("register", cb_delete_load)

clients = list()
for i in range(LOOP_NUMBER):
    c= threading.Thread(target=worker,args=(i+1,))
    clients.append(c)
    c.start()
    time.sleep(1)
        
time.sleep(5)

for x in DBClientDevices.db :
    print(x)
#client.subscribe("casa/teste_2")
#response = client.put("register"," ", cb_put_save)

time.sleep(5)

DBClientDevices.saveToFile("./client_devices.txt")

