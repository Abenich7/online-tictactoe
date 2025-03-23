import socket
import threading
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog
import csv
import time

#class unites client and player functionality 
class TicTacToeClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.game_port = None
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.game_intro()
      

    def game_intro(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("300x800")


        #game instructions paragrpah
        self.instructions = tk.Label(
            self.root, 
            text=
            "Welcome to Tic-Tac-Toe!\n\n"
        "Instructions:\n"
        "1. To play online, enter a game room and wait for an opponent to connect.\n"
        "2. If no opponent enters, select a different room.\n"
        "3. If still no opponent, play single player against the computer.\n\n"
        "Enjoy the game!",
            font=("Arial", 12),
            wraplength=280,
            justify="left")
        self.instructions.pack(pady=10)

        self.start_game_btn = tk.Button(
            self.root,
            text="Start Game",
            command=self.setup_gui,
            font=("Arial", 12)
            )
        self.start_game_btn.pack(pady=20)



    def setup_gui(self):
        
        #destroy the intro screen
        self.instructions.destroy()
        self.start_game_btn.destroy()
  
        self.name_label = tk.Label(self.root, text="Player: ", font=("Arial", 14))
        self.name_label.pack()

      #  self.turn_label = tk.Label(self.root, text="Waiting for game to start...", font=("Arial", 12), fg="blue")
       # self.turn_label.pack()
        
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="blue")
        self.canvas.pack()
        
        self.reset_btn = tk.Button(self.root, 
                                   text="Restart Game", 
                                   command=lambda
                                   p=1: self.reset_game(p),
                                   #add a parameter to the reset_game function

                                   font=("Arial", 12))
        self.reset_btn.pack(pady=5)

        self.quit_btn = tk.Button(self.root, text="Quit Game", command=self.quit_game, font=("Arial", 12), fg="red")
        self.quit_btn.pack(pady=5)

        #callback that starts game
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

   

   
    #if connection to mainserver is successful, move on to selecting game rooms
    def start_game(self):
        #connection request to main server 
        if self.connect_main_server():
            self.start_game_btn.pack_forget()
            self.show_port_buttons()

    
    
    #connect to a game port 
    def show_port_buttons(self):
        for i, port in enumerate([3001, 3002, 3003], 1):
            btn = tk.Button(self.root, 
                          text=f"Enter game room {i}", 
                          #what is a lambda command?
                          command=lambda p=port: self.connect_game_server(p),
                          font=("Arial", 12))
            btn.pack(pady=5)
    

    def connect_game_server(self, port):
        try:
            #connect to port 
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('localhost', port))
            self.game_port = port
            
            data = self.sock.recv(1024).decode('utf-8')
            if data == "name":
                self.name = tk.simpledialog.askstring("Input", "Enter your name:")
                self.sock.send(self.name.encode('utf-8'))
                self.name_label.config(text=f"Player: {self.name}")
            
            
            #wait for game_start message 
            #print waiting for game to start button
            counter = 0
        #   data = self.sock.recv(1024).decode('utf-8')
           
            #wait_label=self.turn_label = tk.Label(self.root, text="Waiting for game to start...", font=("Arial", 12), fg="blue")
            #wait_label.pack()

            data=self.sock.recv(1024).decode('utf-8')  
            if data == "game_active":
                messagebox.showinfo("Game Room Full", "Game room is full. Try another room.")
                return  
            while(data != "game_start"):
                time.sleep(1)
                counter +=1
                if counter==15:
                    
                    self.retry_button = tk.Button(self.root, text="Try Another Game Room", command=self.retry_connection)
                    self.retry_button.pack()
                    return
                data = self.sock.recv(1024).decode('utf-8')

            
            #    messagebox.showinfo("Game Room Full", "Game room is full. Try another room.")
             #   return


            #    if data == "waiting" or data == '':
             #       if counter == 15:
              #          time.sleep(1)
               #         retry_button = tk.Button(self.root, text="Try Another Game Room", command=self.retry_connection)
                #        retry_button.pack()
                 #       return
                    #wait_label.config(text="Waiting for game to start..." + "." * counter)
                    #wait_label.pack()
                  #  counter += 1
                   # data = self.sock.recv(1024).decode('utf-8')
               # if data == "room_full":
                #    messagebox.showinfo("Game Room Full", "Game room is full. Try another room.")
                 #   return
                #else:
                 #   retry_button = tk.Button(self.root, text="Try Another Game Room", command=self.retry_connection)
                  #  retry_button.pack()

                    #reset connection
                   # return
                
            #initialize thread to receive moves from server (runs in parallel to accepting moves from user)
            self.game_start()
            threading.Thread(target=self.receive_moves, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Game server connection error: {e}")
  
    def retry_connection(self):
        # Close the current socket
        if self.sock:
            self.sock.close()
        # Prompt the user to enter a new port
        new_port = tk.simpledialog.askinteger("Input", "Enter a new game room port:")
        if new_port:
            self.connect_game_server(new_port)


    def game_start(self):
         #Print "Game starting" banner on top of board for 3 seconds
         start_btn = tk.Button(self.root, text="Game starting!", font=('Arial', 12))
         start_btn.pack(pady=5)
       #
         self.root.after(3000,start_btn.destroy)# Remove the button after 3 seconds
      #  self.turn_label.config(text="Your Turn" if self.current_player == "X" else "Opponent's Turn")
      #  self.turn_label.pack()
         self.draw_board()
    
    #receive moves made by other players  
    def receive_moves(self):
        while not self.game_over:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if data.startswith('move'):
                    _, row, col = data.split()
                    self.handle_move(int(row), int(col))
                if data == "reset":
                    self.reset_game()
                elif data.startswith('opponent_disconnected'):
                    messagebox.showinfo("Game Over", "Opponent disconnected. Re-enter a game room to play again.")
                    self.reset_game()

                if self.game_over == True:
                    self.reset_game(1)
            except:
                break
   
    #handle moves           
    def handle_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.draw_symbol(col * 100, row * 100)
            
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{self.current_player} Wins!")
                self.game_over = True
                #reset board
                self.board = [["" for _ in range(3)] for _ in range(3)]
                return
                
            self.current_player = "O" if self.current_player == "X" else "X"
            self.save_board()
            
    def on_click(self, event):
        if self.game_over:
            return
            
        col, row = event.x // 100, event.y // 100
        self.sock.send(f"move {row} {col}".encode('utf-8'))

    def quit_game(self):
        self.sock.send("disconnect".encode('utf-8'))
        self.sock.close()
        self.root.quit()

    def reset_game(self,activation=0):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.canvas.delete("all")
        self.draw_board()
        #self.turn_label.config(text="Your Turn")
        if activation==1:
            self.sock.send("reset".encode('utf-8'))
        

        
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
            
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = TicTacToeClient()
    client.run()