import tkinter as tk
from tkinter import messagebox
from .game import ConnectFourGame


class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect 4")
        self.game = ConnectFourGame()
        self.buttons = [tk.Button(self.master, text="Drop", command=lambda col=i: self.drop_piece(col)) for i in range(7)]
        self.create_widgets()

    """Creates the widgets."""
    def create_widgets(self):
        for i, button in enumerate(self.buttons):
            button.grid(row=0, column=i)

        self.canvas = tk.Canvas(self.master, width=700, height=600, bg="blue")
        self.canvas.grid(row=1, columnspan=7)
        self.draw_board()

    """Draws the board."""
    def draw_board(self):
        self.board_circles = []
        for row in range(6):
            row_circles = []
            for col in range(7):
                circle = self.canvas.create_oval(col*100+10, row*100+10, col*100+90, row*100+90, fill="white", outline="black")
                row_circles.append(circle)
            self.board_circles.append(row_circles)

    """Drops a piece in the given column."""
    def drop_piece(self, col):
        if self.game.drop_piece(col):
            self.update_board()
            winner = self.game.check_winner()
            if winner:
                self.handle_game_over(winner)
            elif self.game.is_full():
                self.handle_game_over(None)

    """Handles the end of the game."""
    def handle_game_over(self, winner):
        if winner:
            win_text = f"Joueur {winner} a gagné !"
        else:
            win_text = "Match nul !"

        self.display_game_over_message(win_text)
        self.game.reset_board()
        self.update_board()

    """Displays a message when the game is over."""
    def display_game_over_message(self, message):
        tk.messagebox.showinfo("Fin de la partie", message)

    """Updates the board."""
    def update_board(self):
        for row in range(6):
            for col in range(7):
                piece = self.game.board[row][col]
                color = "white"
                if piece == 1:
                    color = "red"
                elif piece == 2:
                    color = "yellow"

                self.canvas.itemconfig(self.board_circles[row][col], fill=color)

def main():
    root = tk.Tk()
    gui = ConnectFourGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
