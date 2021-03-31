from threading import Thread
import socket

def thread_decorator(func):
    '''
    Torna uma função qualquer uma thread 
    '''
    def __thread(*args,**kwargs):
    
        thread = Thread(target=func, args = args, kwargs = kwargs)
        thread.daemon = True
        thread.start()
        
        
    return __thread


class ListenTCP(Thread):
    def __init__(self,socket,peer):
        Thread.__init__(self,daemon=True)
        self.socket = socket
        self.peer = peer

    def run(self):
        print('Ola {}, sou o seu Servidor programado para ouvir sockets'.format(self.peer.name))

        while 1:
            self.socket.listen(10)
            while 1:
                print("esperando conexão...")
                conn, client = self.socket.accept()
                
                #criando um socket para os jogadores que estão entrando e adicionando
                #os mesmo no dicionário do Par e na lista da Sala de jogo.

                if client[0] not in self.peer.gameroom.connected:
                    self.create_socket_to_send(client[0])
                self.host_connection(conn,client)
                
    
    @thread_decorator
    def host_connection(self,conn,client):
        while 1:
            try:
                msg = conn.recv(2048).decode('utf-8')
                if msg:
                    print('IP[{}] enviou: {}'.format(client[0],msg))
                    reply = 'OK '+msg
                    
                    conn.sendall(reply.encode('utf-8'))

                else:
                    print('perda de conexão')
                    break

            except:
                conn.close()
                print('conexão encerrada')
                break

    def create_socket_to_send(self,ip):
        #Adicionando na lista de endereços conectados na classe GameRoom
        #Para posteriormente outros usuários possão conectar com os jogadores atuais da sala
        self.peer.gameroom.connected.append(ip)

        port =8000
        socketClient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        address=(ip,port)
        socketClient.connect(address)
        if ip not in self.peer.sockets_to_send:
            self.peer.sockets_to_send[ip] = socketClient

