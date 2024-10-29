"""
Tic-Tac-Toe Game with AI and Logging
This script implements a Tic-Tac-Toe game using the Tkinter library for the GUI. 
It includes an AI opponent with different difficulty levels and logs game results.
Modules:
    tkinter: Provides GUI elements.
    random: Used for generating random moves for the AI.
    datetime: Used for timestamping game logs.
    os: Used for file path operations.
Functions:
    print_board(board): Prints the current state of the board to the console.
    check_winner(board, player): Checks if the specified player has won the game.
    is_full(board): Checks if the board is full.
    minimax(board, depth, is_maximizing): Implements the minimax algorithm for the AI.
    best_move(): Determines the best move for the AI based on the selected difficulty.
    random_move(): Returns a random available move.
    on_click(row, col): Handles the event when a cell is clicked.
    reset_board(): Resets the game board for a new game.
    log_game(winner): Logs the game result to a file and in-memory list.
    show_logs(): Displays the game logs in a new window.
Global Variables:
    game_logs: List to store game log entries.
    script_dir: Directory of the current script.
    log_file_path: Path to the log file.
    root: Main Tkinter window.
    board: 3x3 list representing the game board.
    current_player: Tracks the current player ('X' or 'O').
    ai_starts: Flag to alternate the starting player.
    label: Tkinter label to display the current player's turn.
    frame: Tkinter frame to hold the game buttons.
    buttons: 3x3 list of Tkinter buttons for the game grid.
    control_frame: Tkinter frame to hold control buttons and difficulty selector.
    difficulty: Tkinter StringVar to store the selected difficulty level.
    difficulty_menu: Tkinter OptionMenu for selecting difficulty.
    log_button: Tkinter button to show game logs.
    reset_button: Tkinter button to reset the game board.
"""

import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox, Scrollbar
import random
from datetime import datetime
import os

# Initialize the log list
game_logs = []

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "game_logs.txt")

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    # Check rows, columns and diagonals
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
        return best_score

def best_move():
    if difficulty.get() == "Easy":
        return random_move()
    elif difficulty.get() == "Medium":
        if random.random() < 0.5:
            return random_move()
    elif difficulty.get() == "Hard":
        if random.random() < 0.2:
            return random_move()
    best_score = -float('inf')
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

def random_move():
    available_moves = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    return random.choice(available_moves) if available_moves else None

def on_click(row, col):
    global current_player
    if board[row][col] == ' ':
        board[row][col] = current_player
        buttons[row][col].config(text=current_player, fg='blue' if current_player == 'X' else 'red')
        if check_winner(board, current_player):
            messagebox.showinfo("Tic-Tac-Toe", f"Player {current_player} wins!")
            log_game(current_player)
            reset_board()
        elif is_full(board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
            log_game("Tie")
            reset_board()
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            label.config(text=f"Player {current_player}'s turn")
            if current_player == 'O' and difficulty.get() != "Two Players":
                ai_move = best_move()
                if ai_move:
                    on_click(ai_move[0], ai_move[1])

def reset_board():
    global board, current_player, ai_starts
    board = [[' ' for _ in range(3)] for _ in range(3)]
    ai_starts = not ai_starts
    current_player = 'O' if ai_starts else 'X'
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text='', fg='black')
    label.config(text=f"Player {current_player}'s turn")
    if ai_starts and difficulty.get() != "Two Players":
        ai_move = best_move()
        if ai_move:
            on_click(ai_move[0], ai_move[1])

def log_game(winner):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "difficulty": difficulty.get(),
        "winner": winner,
        "first_player": 'O' if ai_starts else 'X'
    }
    game_logs.append(log_entry)
    
    # Write the log entry to the file
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{log_entry['timestamp']} - Difficulty: {log_entry['difficulty']} - Winner: {log_entry['winner']} - First Player: {log_entry['first_player']}\n")

def show_logs():
    log_window = Toplevel(root)
    log_window.title("Game Logs")

    scrollbar = Scrollbar(log_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(log_window, yscrollcommand=scrollbar.set, width=100)
    for log in sorted(game_logs, key=lambda x: x["timestamp"], reverse=True):
        log_entry = f"{log['timestamp']} - Difficulty: {log['difficulty']} - Winner: {log['winner']} - First Player: {log['first_player']}"
        listbox.insert(tk.END, log_entry)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=listbox.yview)

# Initialize the main window
root = tk.Tk()
root.title("Tic Tac Toe!")

# Initialize the game board and current player
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'
ai_starts = False  # Flag to alternate starting player

# Create a label to display the current player's turn
label = tk.Label(root, text=f"Player {current_player}'s turn", font=('Arial', 20))
label.pack()

# Create a frame to hold the buttons
frame = tk.Frame(root)
frame.pack()

# Create buttons for each cell in the Tic-Tac-Toe grid
buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(frame, text=' ', font=('Arial', 40), width=5, height=2,
                                      command=lambda row=row, col=col: on_click(row, col))
        buttons[row][col].grid(row=row, column=col)

# Create a frame to hold the difficulty selector, show logs button, and reset button
control_frame = tk.Frame(root)
control_frame.pack()

# Create a dropdown menu to select the difficulty level
difficulty = tk.StringVar(root)
difficulty.set("Medium")  # Default value
difficulty_menu = tk.OptionMenu(control_frame, difficulty, "Easy", "Medium", "Hard", "Very Hard", "Two Players")
difficulty_menu.pack(side=tk.LEFT)

# Create a button to show the logs
log_button = tk.Button(control_frame, text="Show Logs", command=show_logs)
log_button.pack(side=tk.LEFT)

# Create a reset button
reset_button = tk.Button(control_frame, text="Reset", command=reset_board)
reset_button.pack(side=tk.LEFT)

# Start the main event loop
root.mainloop()
