import tkinter as tk
import random
from tkinter import messagebox

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = {}
        self.mine_positions = set()
        self.create_widgets()
        self.place_mines()
        self.cells_revealed = 0

    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                button = tk.Button(self.master, width=2, height=1, command=lambda r=r, c=c: self.on_click(r, c))
                button.grid(row=r, column=c)
                button.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                self.buttons[(r, c)] = button

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            self.mine_positions.add((r, c))

    def on_click(self, r, c):
        if (r, c) in self.mine_positions:
            self.buttons[(r, c)].config(text="*", bg="red")
            self.game_over()
        else:
            self.reveal(r, c)
            self.check_win()

    def on_right_click(self, r, c):
        button = self.buttons[(r, c)]
        if button['text'] == "F":
            button.config(text="", bg="SystemButtonFace")
        else:
            button.config(text="F", bg="yellow")

    def reveal(self, r, c):
        if (r, c) in self.mine_positions or self.buttons[(r, c)]['state'] == 'disabled':
            return
        self.buttons[(r, c)].config(state='disabled', relief=tk.SUNKEN)
        self.cells_revealed += 1
        mines_around = self.count_mines_around(r, c)
        if mines_around > 0:
            self.buttons[(r, c)].config(text=str(mines_around))
        else:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r + dr < self.rows and 0 <= c + dc < self.cols:
                        self.reveal(r + dr, c + dc)

    def count_mines_around(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in self.mine_positions:
                    count += 1
        return count

    def check_win(self):
        if self.cells_revealed == self.rows * self.cols - self.mines:
            messagebox.showinfo("Congratulations", "You won!")
            self.game_over()

    def game_over(self):
        for (r, c) in self.mine_positions:
            self.buttons[(r, c)].config(text="*", bg="red")
        for button in self.buttons.values():
            button.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()