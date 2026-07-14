import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.status_label = tk.Label(root, text="Player X's Turn", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack()

        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(
                    self.grid_frame,
                    text="",
                    font=("Arial", 24),
                    width=5,
                    height=2,
                    command=lambda r=row, c=col: self.on_click(r, c)
                )
                self.buttons[row][col].grid(row=row, column=col, padx=5, pady=5)

    def check_winner(self, r, c):
        p = self.current_player

        # Check row
        if all(self.board[r][i] == p for i in range(3)):
            return True

        # Check column
        if all(self.board[i][c] == p for i in range(3)):
            return True

        # Check main diagonal
        if r == c and all(self.board[i][i] == p for i in range(3)):
            return True

        # Check secondary diagonal
        if r + c == 2 and all(self.board[i][2 - i] == p for i in range(3)):
            return True

        return False

    def is_draw(self):
        return all(
            self.board[row][col] != ""
            for row in range(3)
            for col in range(3)
        )

    def on_click(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.current_player == "X":
                self.buttons[row][col].config(fg="blue")
            else:
                self.buttons[row][col].config(fg="red")

            if self.check_winner(row, col):
                messagebox.showinfo(
                    "Game Over",
                    f"Player {self.current_player} wins!"
                )
                self.reset_board()

            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_board()

            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(
                    text=f"Player {self.current_player}'s Turn"
                )

    def reset_board(self):
        self.current_player = "X"
        self.status_label.config(text="Player X's Turn")
        self.board = [["" for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", fg="black")


if __name__ == "__main__":
    window = tk.Tk()
    game = TicTacToe(window)
    window.mainloop()