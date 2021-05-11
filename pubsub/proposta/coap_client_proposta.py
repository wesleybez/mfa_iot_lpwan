from threading import Thread
import time
import logging

from infra.coap.user import CoapUser
from infra.coap.device import CoapDevice
from db.db_client_devices import DBClientDevices
from util.json_adapter import JsonAdapter
from infra.coap.query_helper import QueryHelper
from infra.coap.message.message_step_two import CoapMessageStepTwo

from coapthon.client.helperclient import HelperClient

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class CoapClientProposta(Thread):
    def __init__(self,group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None, 
                 id, host, port, fator_mult=10000):

        super(CoapClientProposta,self).__init__(group=group, target=target, 
                                      name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs

        self.id = id
        
        self.host = host
        self.port = port
        
        self.fator_mult = fator_mult
        
        self.client = None
        
        self.medicao = ""
        
    def run(self):
        t_inicio = time.perf_counter()
        #coap client
        client = HelperClient(server=(self.host, self.port))  
        #
        # conectar ao servico de autenticacao e obter credencial
        #
        #envio das credenciais
        usuario = CoapUser(DBClientDevices.db[self.id]["user"],
                       DBClientDevices.db[self.id]["passwd"])
        response = client.post("login", usuario.toJSON(), self.process_post_login, 10)
        if response is not None:
            print (response.pretty_print())
        t_connection = time.perf_counter()
        td_connection = t_connection - t_inicio 
        # client.put("teste", "aleatorio_"+str(cont), cb_put(), 10)    
        t_publish = time.perf_counter() 
        td_publish = t_publish - t_connection
        #
        #time.sleep(1000)
        #client.subscribe("casa/teste_2")
        #response = client.get(path2)
        #print response.pretty_print()
        #time.sleep(1000)
        t_subscribe = time.perf_counter() 
        td_subscribe = t_subscribe - t_publish
        #client.stop()
        t_disconnect = time.perf_counter()
        td_disconnect = t_disconnect - t_subscribe
    
        self.medicao = " "+str(self.id+1)
        +","+str(t_inicio*self.fator_mult)
        +","+str(td_connection*self.fator_mult)
        +","+str(td_publish*self.fator_mult)
        +","+str(td_subscribe*self.fator_mult)
        +","+str(td_disconnect*self.fator_mult)
        +"\n"

    
    def process_post_login(self,response):
        """ funcao de callback do post de autenticação passo 1 """
        logger.debug ("dentro do callback do put do passo1")
        print("response:",response)
        a = JsonAdapter.convertToDict(response.payload)
        print(a)
        query=a["query"]
    
        if(query!=1):
            resultado = QueryHelper.processQuery(query, DBClientDevices.db[id]["uuid"])
            print("resultado query:", resultado)        
            query_result= CoapMessageStepTwo(str(resultado,"utf-8"),a["auth_code"])
            self.client.post("login", query_result.toJSON(), self.process_post_step2, 10)
        else :
            print("sem segundo fator")
    
    def process_post_step2(self,response):
        """ funcao de callback do post de autenticação passo 1 """
        logger.debug ("dentro do callback do put do passo2")
        print("response:",response)
        a = JsonAdapter.convertToDict(response.payload)
        print(a)