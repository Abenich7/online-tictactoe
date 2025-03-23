import socket
import threading
import time

class GameRoom:
    def __init__(self):
        self.players = []
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = None
        self.game_active = False

class TicTacToeServer:
    def __init__(self, host="127.0.0.1", main_port=3000):
        self.host = host
        self.main_port = main_port
        self.game_ports = [3001, 3002, 3003]
        self.game_rooms = {port: GameRoom() for port in self.game_ports}
        
        # Start main server
        self.main_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_server.bind((host, main_port))
        self.main_server.listen(5)
        print(f"Main server listening on {host}:{main_port}")
        
        # Start game servers
        for port in self.game_ports:
            threading.Thread(target=self.start_game_server, args=(port,)).start()

    def start_game_server(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, port))
        server.listen(5)
        print(f"Game server started on port {port}")
        
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client, port)).start()

    def handle_client(self, client, port):
        try:
            # Get player name
            client.send("name".encode('utf-8'))
            name = client.recv(1024).decode('utf-8')
            
            room = self.game_rooms[port]
            if len(room.players) < 2:
                room.players.append((name, client))
                if len(room.players) == 2:
                    self.start_game(port)
            else:
                client.send("room_full".encode('utf-8'))
                client.close()
                
        except Exception as e:
            print(f"Error handling client: {e}")
            client.close()

    def start_game(self, port):
        room = self.game_rooms[port]
        room.game_active = True
        room.current_turn = room.players[0][0]
        
        # Notify players game is starting
        for name, client in room.players:
            client.send(f"game_start {name}".encode('utf-8'))
            threading.Thread(target=self.handle_game, args=(name, client, port)).start()

    def handle_game(self, player_name, client, port):
        room = self.game_rooms[port]
        
        while room.game_active:
            try:
                data = client.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                if data.startswith('move') and player_name == room.current_turn:
                    _, row, col = data.split()
                    row, col = int(row), int(col)
                    
                    if room.board[row][col] == '':
                        room.board[row][col] = 'X' if player_name == room.players[0][0] else 'O'
                        self.broadcast_move(port, row, col)
                        room.current_turn = room.players[1][0] if room.current_turn == room.players[0][0] else room.players[0][0]
                
                elif data == "reset":
                    room.board = [['' for _ in range(3)] for _ in range(3)]
                    room.current_turn = room.players[0][0]
                    self.broadcast_reset(port)
                    
            except Exception as e:
                print(f"Game error: {e}")
                break
                
        self.handle_disconnect(player_name, port)

    def broadcast_move(self, port, row, col):
        room = self.game_rooms[port]
        for _, client in room.players:
            client.send(f"move {row} {col}".encode('utf-8'))

    def broadcast_reset(self, port):
        room = self.game_rooms[port]
        for _, client in room.players:
            client.send("reset".encode('utf-8'))

    def handle_disconnect(self, player_name, port):
        room = self.game_rooms[port]
        room.game_active = False
        for name, client in room.players:
            if name != player_name:
                client.send("opponent_disconnected".encode('utf-8'))
        room.players = []
        room.board = [['' for _ in range(3)] for _ in range(3)]

if __name__ == "__main__":
    server = TicTacToeServer()
    while True:
        client, addr = server.main_server.accept()
        client.send(f"ports{server.game_ports}".encode('utf-8'))
        client.close()