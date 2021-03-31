class GameRoom():
    def __init__(self,name,ip):
        self.name = name
        self.connected = [ip,]
        self.peer_with_permission = ip

    

    def __str__(self):
        return 'GameRoom( {},{} )'.format(self.name,self.connected)

    def __repr__(self):
        return '('+str(self.name)+','+str(self.connected)+')'


