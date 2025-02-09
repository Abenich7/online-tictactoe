import socket
import threading
# SERVER 
import time

#client connects to TicTacToe server
HOST, MAIN_PORT = "127.0.0.1", 3000
available_ports=[3001,3002,3003]

#MySocket class inherits from socket.socket (subclass)
class MySocket(socket.socket):
    
    def __init__(self,port=None, sock=None):
        
        if sock is None:
            # If no socket provided, create a new one
            super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        else:
            # If socket provided, use its file descriptor to initialize
            super().__init__(fileno=sock.fileno())
        
        #child server
        if port is not None:
            self.bind(('localhost', port))
            self.listen()
            print(f"[*] Child server started on port {port}")
            self.clients=[]
            self.waiting_room={}
            self.players={}
            self.games={}

        #main server
        if port == 3000:
            self.bind(('localhost', port))
            #send available ports 
            self.mysend(available_ports)
        
            print(f"[*] Main server listening on {HOST}:{port}")
        
    # def connect(self, host, port):
     #   self.sock.connect((host, port))
    def listen(self):
        
        while True: 
            self.listen(5)
            try:
                #does accept wait for new client to connect to running thread? 
                client_socket, address = self.accept()
            except Exception as e:
                print(f"Error accepting connection: {e}")
            print(f"[*] Accepted connection from {address}")
            client_socket = MySocket(sock=client_socket_temp)
            #add client to list of clients
            self.clients.append(client_socket)
            #get client name
            client_socket.mysend("name")
            name=client_socket.myreceive()
            print(f"[*] Client name: {name}")
            self.clients.append(name)
            try:
                threading.Thread(target=self.handle,args=[client_socket,]).start()
            except Exception as e:
                print(f"Error receiving data: {e}")
            #client_socket.myreceive()
            #client_socket.myaccept()
            #client_socket.myreceive

    def mysend(self, msg,port):
        # Pad the message to the fixed length
        if port==MAIN_PORT:
            #make message that starts with word "ports" and then list of available ports
            msg="ports"+str(available_ports)
            msg.encode('utf-8')
            #self.close()
        else:
            if type(msg) == str:
                msg.encode('utf-8')
            else:
                msg = str(msg).encode('utf-8')
        self.send(msg)
        

    def myreceive(self,MSGLEN=1024):
        #while True:
         #   chunks = []
          #  bytes_recd = 0
           # while bytes_recd < MSGLEN:
            #    chunk = self.recv(min(MSGLEN - bytes_recd, 2048))
             #   if chunk == b'':
              #      raise RuntimeError("socket connection broken")
                
               # chunks.append(chunk)
                #bytes_recd = bytes_recd + len(chunk)
            #print("Received: {}".format(chunks.strip()))
            #return b''.join(chunks)
            self.recv()
            return self.recv()

        
    def handle_multiplayer(self, name, message):
        if message.decode("utf-8") == "multiplayer":
            # Add player to waiting room
            self.waiting_room[name] = True
        
            time_waited = 0
            while name in self.waiting_room:
                # Look for available players
                for player in self.waiting_room:
                    if player != name:
                        # Find empty game room
                        for game_room, players in self.games.items():
                            if not players:  # Empty game room
                                self.games[game_room] = [name, player]
                                del self.waiting_room[name]
                                del self.waiting_room[player]
                                return
            
                time.sleep(1)
                time_waited += 1
            
                # Timeout after 10 seconds
                if time_waited > 10:
                    self.client_socket.mysend("no players")
                    self.client_socket.close()
                    break
            
        if message.decode("utf-8") == "start":
                #split message into strings
                word1,word2=message.split("",1)
                #2 player game
                if word2=="2":
                    self.mysend("2 player game")
                if word2=="3":
                    self.mysend("3 player game")
                if word2=="4":
                    self.mysend("4 player game")


                
        if message.decode("utf-8") == "shape":
                message, shape = message.split(" ", 1)
                self.players[name]=shape

        if message.decode("utf-8") == "move":
                break
            #get first and second string from data
            #first string is name of client
            #second string is message
        if message.decode("utf-8") == "quit":
                #remove client
                self.clients.remove(name)
                #close socket
                client_socket.close()
                break
            

    
            


 
    def myaccept(self):
        """
        Override accept to return MySocket instance instead of regular socket.
        Returns: (MySocket, address)
        """
        client_socket, address = super().accept()
        return client_socket, address
    
    
        