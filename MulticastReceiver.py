from threading import Thread
import pickle
import socket



class MulticastReceiver(Thread):
    '''
    Essa classe trata de receber a mensagem do usuário que tem a permissão para passar
    a sala de jogo decodifica com auxilio da biblioteca pickle e adiciona a sala na variavel
    de salas disponíveis (rooms_available) para o usuário poder entrar, usando thread para rodar
    em paralelo com o programa principal
    '''
    def __init__(self,socket,peer):
        '''
        Inicializador da classe MulticastReceiver
        '''
        Thread.__init__(self,daemon=True)
        self.peer = peer
        self.socket = socket

    def run(self):
        '''
        Enquanto o usuário não estiver em jogo, ele irá receber mensagens de salas diferentes
        pelos seus respectivos usuários com permissão de passa-las, e irá por essas salas em uma
        lista de salas disponíveis    
        '''
        while 1:
            while self.peer.playerstate() == 'not in game':
                data, address = self.socket.recvfrom(4096)
                data = pickle.loads(data)
                self.rooms_update(data)

            

    def rooms_update(self,room):
        '''
        Faz a atualização das salas onlines
        '''
        flag = True

        if len(self.peer.rooms_available) == 0:
            self.peer.rooms_available.append(room)
        else:
            for i in range (len(self.peer.rooms_available)):
                if self.peer.rooms_available[i].name == room.name:
                    self.peer.rooms_available[i] = room
                    flag= False
                    break
        
            if flag:
                self.peer.rooms_available.append(room)
    





