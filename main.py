import tkinter as tk
from tkinter import messagebox

# Game settings
ROWS, COLUMNS = 6, 7
PLAYER_1, PLAYER_2 = "red", "yellow"
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 10

# Initialize the game board (6 rows x 7 columns) with empty cells
board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
current_player = PLAYER_1

# Initialize the tkinter window
root = tk.Tk()
root.title("Connect Four")
canvas = tk.Canvas(root, width=COLUMNS * CELL_SIZE, height=(ROWS + 1) * CELL_SIZE, bg="blue")
canvas.pack()

# Function to draw the empty board
def draw_board():
    canvas.delete("all")
    for row in range(ROWS):
        for col in range(COLUMNS):
            x1 = col * CELL_SIZE + CELL_SIZE // 2
            y1 = (row + 1) * CELL_SIZE + CELL_SIZE // 2
            canvas.create_oval(x1 - RADIUS, y1 - RADIUS, x1 + RADIUS, y1 + RADIUS, fill="white", outline="black")

# Function to reset the board
def reset_game():
    global board, current_player
    board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_player = PLAYER_1
    draw_board()
    messagebox.showinfo("Game Reset", "New Game! Player 1 (Red) starts.")

# Function to check if the current move wins the game
def winning_move(row, col, piece):
    # Check directions: Horizontal, Vertical, Diagonal /
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 0
        for i in range(-3, 4):  # Check in both directions
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == piece:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
    return False

# Function to handle column clicks
def handle_click(event):
    global current_player
    col = event.x // CELL_SIZE
    if col < 0 or col >= COLUMNS:
        return

    # Find the next available row in the clicked column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] is None:
            board[row][col] = current_player
            x1 = col * CELL_SIZE + CELL_SIZE // 2
            y1 = (row + 1) * CELL_SIZE + CELL_SIZE // 2
            canvas.create_oval(x1 - RADIUS, y1 - RADIUS, x1 + RADIUS, y1 + RADIUS, fill=current_player)

            # Check if the move wins the game
            if winning_move(row, col, current_player):
                messagebox.showinfo("Game Over", f"Player {1 if current_player == PLAYER_1 else 2} wins!")
                reset_game()
                return

            # Check for a tie
            if all(board[r][c] is not None for r in range(ROWS) for c in range(COLUMNS)):
                messagebox.showinfo("Game Over", "It's a tie!")
                reset_game()
                return

            # Switch players
            current_player = PLAYER_2 if current_player == PLAYER_1 else PLAYER_1
            return

# Bind canvas clicks to handle click events
canvas.bind("<Button-1>", handle_click)

# Draw initial empty board and create a reset button
draw_board()
reset_button = tk.Button(root, text="Reset Game", command=reset_game)
reset_button.pack()

# Run the tkinter main loop
root.mainloop()
