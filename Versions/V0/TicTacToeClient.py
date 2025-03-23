import socket
import threading
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog
import csv

class TicTacToeClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.game_port = None
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.setup_gui()
      #  self.connect_main_server()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("300x500")
        
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="blue")
        self.canvas.pack()
        
        self.reset_btn = tk.Button(self.root, text="Restart Game", command=self.reset_game, font=("Arial", 12))
        self.reset_btn.pack(pady=5)
        
        self.start_game_btn = tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 12))
        self.start_game_btn.pack(pady=5)
        
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        
    def connect_main_server(self):
        try:
            self.sock.connect(('localhost', 3000))
            data = self.sock.recv(1024).decode('utf-8')
            if data.startswith('ports'):
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")
            return False
            
    def start_game(self):
        if self.connect_main_server():
            self.start_game_btn.pack_forget()
            self.show_port_buttons()
            
    def show_port_buttons(self):
        for i, port in enumerate([3001, 3002, 3003], 1):
            btn = tk.Button(self.root, 
                          text=f"Choose game room {i}", 
                          command=lambda p=port: self.connect_game_server(p),
                          font=("Arial", 12))
            btn.pack(pady=5)
            
    def connect_game_server(self, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('localhost', port))
            self.game_port = port
            
            data = self.sock.recv(1024).decode('utf-8')
            if data == "name":
                self.name = tk.simpledialog.askstring("Input", "Enter your name:")
                self.sock.send(self.name.encode('utf-8'))
                
            threading.Thread(target=self.receive_moves, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Game server connection error: {e}")
            
    def receive_moves(self):
        while not self.game_over:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if data.startswith('move'):
                    _, row, col = data.split()
                    self.handle_move(int(row), int(col))
            except:
                break
                
    def handle_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.draw_symbol(col * 100, row * 100)
            
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{self.current_player} Wins!")
                self.game_over = True
                return
                
            self.current_player = "O" if self.current_player == "X" else "X"
            self.save_board()
            
    def on_click(self, event):
        if self.game_over:
            return
            
        col, row = event.x // 100, event.y // 100
        self.sock.send(f"move {row} {col}".encode('utf-8'))
        
    def draw_board(self):
        for i in range(1, 3):
            self.canvas.create_line(i * 100, 0, i * 100, 300, fill="white", width=5)
            self.canvas.create_line(0, i * 100, 300, i * 100, fill="white", width=5)
            
    def draw_symbol(self, x, y):
        if self.current_player == "X":
            padding = 20
            self.canvas.create_line(x + padding, y + padding, 
                                  x + 100 - padding, y + 100 - padding, 
                                  fill="red", width=5)
            self.canvas.create_line(x + 100 - padding, y + padding, 
                                  x + padding, y + 100 - padding, 
                                  fill="red", width=5)
        else:
            self.canvas.create_oval(x + 20, y + 20, x + 80, y + 80, 
                                  outline="green", width=5)
                                  
    def check_winner(self):
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)): return True
            if all(self.board[j][i] == self.current_player for j in range(3)): return True
        
        if all(self.board[i][i] == self.current_player for i in range(3)): return True
        if all(self.board[i][2-i] == self.current_player for i in range(3)): return True
        return False
        
    def save_board(self):
        with open('data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.board)
            
    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.canvas.delete("all")
        self.draw_board()
        self.sock.send("reset".encode('utf-8'))
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = TicTacToeClient()
    client.run()