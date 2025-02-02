import MySocket

#server to inherit from MySocket and add methods for instantiating 
#client sockets 

class MySrv(MySocket.MySocket):
       
    def myaccept(self):
        #implement custom myaccept method
        while True:
            clientsocket, address = self.accept()
            return clientsocket, address
            
        

    