from Peer import Peer
from GameRoom import GameRoom
import time
import socket

def main():
    '''
    Função responsável pela navegação do usuário perante as funções disponíveis na classe
    Peer, a função principal do programa
    '''
    name = input('Digite o nome do seu usuário: ')
    your_ip = input("Digite seu Ip: ")
    peer = Peer(name,your_ip)
    flag = True
    print('Bem vindo ao lobby {}, você pode fazer as seguintes ações: \n'.format(peer.name))
    print_menu()

    while flag:
        peer.receive_multicast()
        option = menu()
        flag = option_select(option,peer)






def option_select(option,peer):
    try:
        if option == 1:
            flag1 = True
            for i in range(len(peer.rooms_available)):
                print('Identificador ({}) {}'.format(i,peer.rooms_available[i].name))
                flag1 = False


            if flag1:
                print('Não há salas disponíveis')
            return True

        elif option == 2:


            
            room_number = int(input("Digite o número da sala que você quer entrar: " ))
            if room_number in range(len(peer.rooms_available)):
                peer.gameroom = peer.rooms_available[room_number]

                #Adicionando o ip do seu usuário na lista de usuários presentes na sala
                peer.gameroom.connected.append(peer.your_ip)
                peer.gaming = True
                peer.rooms_available = []


                peer.listenning()
                peer.send_multicast()

                time.sleep(0.2)
                peer.starting()
                send_for_all(peer)
                return False




            else:
                print('Não existe a sala que você está procurando')
                return True

           
        elif option == 3:
            while 1:
                name_room = input('Digite o Nome da sala: ')
                room = GameRoom(name_room,peer.your_ip)
                peer.gameroom = room
                peer.gaming = True #Sinaliza que ele está em jogo agora
                peer.rooms_available = [] #apaga todo o cache de salas disponíveis

                #Depois de criar a sala ele irá ouvir por um socket TCP
                peer.listenning()

                #Trocar a flag dele, dizendo que ele possui permissão para enviar a sala
                #e começar a enviar a sala via multicast
                peer.permission_flag = True
                peer.send_multicast()
                time.sleep(0.2) #arrumar a printagem na tela


                print('Digite /sair, se quiser sair da sala.')
                send_for_all(peer)
                return False





        elif option == 4:
            print_menu()
            return True
        elif option == 5:
            print('Saindo do jogo ')
            return False
    except:
        print('Occoreu um erro desconhecido\nFechando o jogo')
        return False

def print_menu():
    '''
    Printa as ações que o usuário pode fazer e seu código 
    '''
    print('Listar salas onlines - Digite 1')
    print('Entrar em uma sala online - Digite 2')
    print('Criar uma sala - Digite 3')
    print('Visualizar menu - Digite 4')
    print('Sair - Digite 5')

def menu():
    '''
    Faz a filtagrem de opções possiveis de se escolher e dá retorno 
    com a opção selecionada
    '''

    list_options =['1','2','3','4','5']
    
    option = input('\nO que Você deseja fazer agora?\n>>>')
    while option not in list_options:
        option = input('Você digitou um comando invalido\nDigite novamente: ')

    return int(option)

def send_for_all(peer):
    while 1:
        message = input('Digite sua mensagem: ')
        if message.lower() == '/sair':
            return
        else:
            if len(peer.sockets_to_send) == 0:
                print('Ninguem está lhe escutando')
            else:
                #para evitar erros no for crei uma copia do dicionario dos sockets
                #para ser identado, pelo fato de ter chances de algum elemento ser excluido
                copy_sockets_to_send = dict.copy(peer.sockets_to_send) 
                for i in copy_sockets_to_send:
                    try:
                        peer.sockets_to_send[i].send(message.encode("utf-8"))
                        reply = peer.sockets_to_send[i].recv(2048)


                    except:
                        print("Você perdeu a conexão com {}".format(i))
                        del peer.sockets_to_send[i]
                        print (peer.gameroom.connected )
                        peer.gameroom.connected.remove(i)

                        #Verificando se o par deletando era o par com permissão para passar a sala
                        #para os outros usuários, se for, será subistituido por outro
                        if i == peer.gameroom.peer_with_permission:

                            print(peer.gameroom.peer_with_permission,peer.gameroom.connected )
                            peer.gameroom.peer_with_permission = peer.gameroom.connected[0]

                            if peer.your_ip == peer.gameroom.peer_with_permission:
                                peer.permission_flag = True


main()