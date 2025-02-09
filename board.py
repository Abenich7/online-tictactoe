import tkinter as tk
from tkinter import messagebox
import csv
from Client1_old import MySocket


client=MySocket()

# Initialize game state
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False

# Create main window
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("300x500")

# Create a canvas for the game board
canvas = tk.Canvas(root, width=300, height=300, bg="blue")
canvas.pack()

# Function to draw the board lines
def draw_board():
    for i in range(1, 3):
        canvas.create_line(i * 100, 0, i * 100, 300, fill="white", width=5)  # Vertical
        canvas.create_line(0, i * 100, 300, i * 100, fill="white", width=5)  # Horizontal

# Function to draw X
def draw_x(x, y):
    padding = 20
    canvas.create_line(x + padding, y + padding, x + 100 - padding, y + 100 - padding, fill="red", width=5)
    canvas.create_line(x + 100 - padding, y + padding, x + padding, y + 100 - padding, fill="red", width=5)

# Function to draw O
def draw_o(x, y):
    canvas.create_oval(x + 20, y + 20, x + 80, y + 80, outline="green", width=5)

# Function to check for a win
def winning_move(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True  # Rows
        if all(board[j][i] == player for j in range(3)): return True  # Columns

    if all(board[i][i] == player for i in range(3)): return True  # Diagonal
    if all(board[i][2 - i] == player for i in range(3)): return True  # Anti-diagonal

    return False


# Function to save the current board state to data.csv
def save_board_to_csv():
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(board)



# Function to handle mouse clicks
def on_click(event):
    global current_player, game_over

    if game_over:
        return

    col, row = event.x // 100, event.y // 100

    if board[row][col] == "":
        board[row][col] = current_player
        (draw_x if current_player == "X" else draw_o)(col * 100, row * 100)

        if winning_move(current_player):
            messagebox.showinfo("Game Over", f"{current_player} Wins!")
            game_over = True
            return

        current_player = "O" if current_player == "X" else "X"

    save_board_to_csv()
    #call 

def start_game():
    #send message to server to start game
    client.mysend("start".encode('utf-8'))

    #hide start game button
    start_game_btn.pack_forget()
    #show choose ports buttons
    choose_ports()

def choose_ports():
    #3 buttons to choose game room
    tk.Button(root, text="Choose game room 1", command=port1, font=("Arial", 12)).pack(pady=5)
    tk.Button(root, text="Choose game room 2", command=port2, font=("Arial", 12)).pack(pady=5)
    tk.Button(root, text="Choose game room 3", command=port3, font=("Arial", 12)).pack(pady=5)

def port1():
    #send message to server to choose port 1
    client.mysend("port1".encode('utf-8'))

def port2():
    #send message to server to choose port 2
    client.mysend("port2".encode('utf-8'))

def port3():
    #send message to server to choose port 3
    client.mysend("port3".encode('utf-8'))

    
    



# Function to reset the game
def reset_game():
    global board, current_player, game_over
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    canvas.delete("all")
    draw_board()


# Reset Button
reset_btn = tk.Button(root, text="Restart Game", command=reset_game, font=("Arial", 12))
reset_btn.pack(pady=5)

#start game button
start_game_btn = tk.Button(root, text="Start Game", command=start_game, font=("Arial", 12))
start_game_btn.pack(pady=5)


# Draw board and bind click events
draw_board()
canvas.bind("<Button-1>", on_click)

# Run the Tkinter event loop
root.mainloop()


