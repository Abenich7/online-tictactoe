import tkinter as tk
from tkinter import messagebox



# Initialize game state
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False

# Create main window
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("300x350")

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

# Draw board and bind click events
draw_board()
canvas.bind("<Button-1>", on_click)

# Run the Tkinter event loop
root.mainloop()


