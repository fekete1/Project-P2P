import pickle
import socket
import time
from threading import Thread




class MulticastSender(Thread):
    '''
    Envia a sala que o usuário (objeto Peer) está no momento
    com auxlio da classe Thread para ser feito paralelamente ao programa
    principal
    '''
    def __init__(self,socket,peer):
        """
        Inicializador da classe MulticastSender
        """
        Thread.__init__(self, daemon=True)
        self.peer = peer
        self.socket = socket

    def run(self):
        '''
        Método que define como a Thread irá se comportar quando inicializada
        Ele irá comprimir a sala (Classe GameRoom) que o usuário está usando biblioteca pickle
        e enviar via multicast para usuários que estão ouvindo, ou seja aqueles que não estão em
        uma sala, de 1 em 1 segundo, porém isso so acontecerá se o usuário tiver permissão para passar
        a sala, com seu atributo "permission_flag" como True.
        '''

        multicast_ip = '224.0.0.1'
        multicast_port = 9000
        multi_address = (multicast_ip,multicast_port)
        while 1:
            message = pickle.dumps(self.peer.gameroom)

            while self.peer.permission_flag:
                self.socket.sendto(message,multi_address)

                time.sleep(1)

