from MulticastReceiver import MulticastReceiver
from MulticastSender import MulticastSender
from ListenTCP import *
import time
import socket



class Peer():
    def __init__(self,name,ip):
        self.name = name
        self.gaming = False
        self.gameroom =''
        self.your_ip = ip

        #Avisa se ele possui a permissão para passar a sala
        self.permission_flag = False

        self.rooms_available =[]
        self.del_rooms_available_cache() #metodo para apagar o cache de salas disponiveis

        self.sockets_to_send= {}


        #Socket Servidor TCP
        self.IP = ''
        self.port= 8000
        self.socketServer = socket.socket()
        self.socketServer.bind(('',self.port))

        #Socket Envia mensagens Multicast UDP
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



 
        #Socket Recebe mensagens Multicast UDP porta 9000
        multicast_ip = '224.0.0.1'
        interface_ip = self.your_ip

        self.sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        mgroup = socket.inet_aton(multicast_ip) + socket.inet_aton(interface_ip)
        self.sock_receive.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mgroup)
        self.sock_receive.bind((interface_ip,9000))

    def listenning(self):
        listen = ListenTCP(self.socketServer,self)

        listen.start()
        


    def send_multicast(self):
        send= MulticastSender(self.sock_send,self)
        
        send.start()

        


    def receive_multicast(self):
        receive = MulticastReceiver(self.sock_receive,self)

        receive.start()

        
    
    def starting(self):
        port = 8000
        for i in self.gameroom.connected:
            if i != self.your_ip:
                socketClient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                socketClient.connect((i,port))
                self.sockets_to_send[i] = socketClient

        print(self.sockets_to_send)

    @thread_decorator
    def del_rooms_available_cache(self):
        '''
        Apaga o cache de salas disponíveis a cada 10 segundos rodando em
        paralelo ao programa principal
        '''
        while 1:
            self.rooms_available = []
            time.sleep(10)
    
    def playerstate(self):
        '''
        Retorna a situação atual do par sobre o seu estado 
        '''
        if self.gaming and self.gameroom:
            return "playing"
        elif not self.gaming and self.gameroom:
            return "watching"
        else:
            return "not in game"
    



















    