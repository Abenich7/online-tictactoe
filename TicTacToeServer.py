import socket
import threading
import time

#create GameRoom class to store game data rather than using global variables and maintaing a dictionary
class GameRoom:
    def __init__(self):
        self.players = []
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.game_active = False
        self.current_player = None

#Create TicTacToeServer class to handle the server side of the game
class TicTacToeServer:
    #initialize the server with the host and main port
    def __init__(self, host="127.0.0.1", main_port=3000):
        self.host = host
        self.main_port = main_port
        #initialize the game ports and game rooms
        self.game_ports = [3001, 3002, 3003]
        #initialize the game rooms with the game ports
        self.game_rooms = {port: GameRoom() for port in self.game_ports}
        
        # Start main server
        self.main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_server.bind((host, main_port))
        self.main_server.listen(5)
        print(f"Main server listening on {host}:{main_port}")
        
        # Dispatch game servers as threads
        for port in self.game_ports:
            threading.Thread(target=self.start_game_server, args=(port,)).start()

    #start the game server on the given port
    def start_game_server(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, port))
        server.listen(5)
        print(f"Game server started on port {port}")
        
        #when new client connects, dispatch new thread to handle the client
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client, port)).start()

    #handle the client connection
    def handle_client(self, client, port):
        try:
            # Get player name
            client.send("name".encode('utf-8'))
            name = client.recv(1024).decode('utf-8')
            
            # get the game room
            room = self.game_rooms[port]

            
            #if the room has less than 2 players, add the player to the room
           # if len(room.players) < 2:
                #append to list tuple (name,client)
            if room.game_active == False:
                room.players.append((name, client))

            else:
                client.send("game_active".encode('utf-8'))
                #if the room has 1 player,notify them
               # if len(room.players) == 1:
                  #  client.send("waiting".encode('utf-8'))  

                #if the room has 2 players, start the game
            if len(room.players) == 2:
                    #called once by the second player that enters the room (he activates it)
                self.start_game(port)

            

                # check if the same player is trying to connect again

         #       client.send("room_full".encode('utf-8'))
          
          #      client.close()
                

            #check if there are duplicate players in the room
           # if len(room.players) == 2:
                #check if same client is trying to connect again
            #    for name,client in room.players:
             #       name_one=name
              #      client_one=client
                    #compare next name to other players in room
               #     for name,client in room.players:
                #        if name_one==name:
                            #remove the player from the room
                 #           room.players.remove((name,client))  

                    #append to list tuple (name,client)
                  #  room.players.append((name, client))
                    
            
        except Exception as e:
            print(f"Error handling client: {e}")
            client.close()

    #following method is called when there are two clients in the game room
    def start_game(self, port):
        room = self.game_rooms[port]
        room.game_active = True
        room.current_player = room.players[0][0]
        
        # Notify players game is starting
        for name, client in room.players:
            #notify client game is starting
            client.send("game_start".encode('utf-8'))
            threading.Thread(target=self.handle_game, args=(name, client, port)).start()

    #following method is the game loop, which all clients enter around the same time
    def handle_game(self, player_name, client, port):
        room = self.game_rooms[port]
        
        while room.game_active:
            try:
                data = client.recv(1024).decode('utf-8')
                if not data:
                    break
                # client moves 
                if data.startswith('move') and player_name == room.current_player:
                    _, row, col = data.split()
                    row, col = int(row), int(col)
                    
                    if room.board[row][col] == '':
                        room.board[row][col] = 'X' if player_name == room.players[0][0] else 'O'
                        #broadcast moves to toher players
                        self.broadcast_move(port, row, col)
                        room.current_player = room.players[1][0] if room.current_player == room.players[0][0] else room.players[0][0]
                
                #check for winner
                    if self.check_winner(port):
                            self.broadcast_winner(port, room.current_player)
                            time.sleep(3)  # Delay before restarting
                            self.broadcast_reset(port)


                if data == "reset":
                    room.board = [['' for _ in range(3)] for _ in range(3)]
                    room.current_player = room.players[0][0]
                    self.broadcast_reset(port)

                if data == "disconnect":
                    self.handle_disconnect(player_name, port)
                    break
                    
            except Exception as e:
                print(f"Game error: {e}")
                break
                
        self.handle_disconnect(player_name, port)
    #broadcast move to other players in room
    def broadcast_move(self, port, row, col):
        room = self.game_rooms[port]
        for _, client in room.players:
            client.send(f"move {row} {col}".encode('utf-8'))

    def broadcast_winner(self, port, winner_name):
        room = self.game_rooms[port]
        for _, client in room.players:
            client.send(f"winner {winner_name}".encode('utf-8'))


    def broadcast_reset(self, port):
        room = self.game_rooms[port]
        for _, client in room.players:
            client.send("reset".encode('utf-8'))

    def handle_disconnect(self, player_name, port):
        room = self.game_rooms[port]
        room.game_active = False
        remaining_players = [p for p in room.players if p[0] != player_name]

        for name, client in remaining_players:
            if name != player_name:
                client.send("opponent_disconnected".encode('utf-8'))
        room.players = []
        room.board = [['' for _ in range(3)] for _ in range(3)]

    def check_winner(self,port):
        room=self.game_rooms[port]
        for i in range(3):
            if all(room.board[i][j] == room.current_player for j in range(3)): return True
            if all(room.board[j][i] == room.current_player for j in range(3)): return True
        
        if all(room.board[i][i] == room.current_player for i in range(3)): return True
        if all(room.board[i][2-i] == room.current_player for i in range(3)): return True
        return False
        

if __name__ == "__main__":
    server = TicTacToeServer()
    while True:
        #run main server
        client, addr = server.main_server.accept()
        client.send(f"ports{server.game_ports}".encode('utf-8'))
        client.close()