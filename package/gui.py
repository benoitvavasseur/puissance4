# gui.py
import tkinter as tk
from tkinter import messagebox

from package.reinforcement.qLearning import QLearningAlgorithm
from .game import ConnectFourGame
import time

class ConnectFourGUI:
    def __init__(self, master, player1_algorithm=None, player2_algorithm=None):
        self.master = master
        self.master.title("Connect 4")
        self.game = ConnectFourGame()
        self.player1_algorithm = player1_algorithm
        self.player2_algorithm = player2_algorithm
        self.buttons = [tk.Button(self.master, text="Drop", command=lambda col=i: self.drop_piece(col)) for i in range(7)]
        self.create_widgets()
        self.on_close_callbacks = []

    def add_on_close_callback(self, callback):
        self.on_close_callbacks.append(callback)

    def close(self):
        print("Closing the application and calling callbacks")
        for callback in self.on_close_callbacks:
            callback()
        self.master.destroy()

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
        available_columns = [i for i in range(7) if self.game.board[0][i] == 0]
        # Current state before playing
        current_state = str(self.game.board)
        if self.player1_algorithm is not None and self.game.current_player == 1:
            # Player 1 is an AI
            column = self.player1_algorithm.get_next_move(self.game.board, available_columns)
        elif self.player2_algorithm is not None and self.game.current_player == 2:
            # Player 2 is an AI
            column = self.player2_algorithm.get_next_move(self.game.board, available_columns)
        else:
            # Players are human
            column = col

        if self.game.drop_piece(column):
            self.update_board()

            winner = self.game.check_winner()
            done = winner is not None or self.game.is_full()

            # Update of table Q only if the agent is of type QLearningAlgorithm
            current_player_agent = self.player1_algorithm if self.game.current_player == 1 else self.player2_algorithm
            if isinstance(current_player_agent, QLearningAlgorithm):
                reward = self.calculate_reward_qLearning(winner, done)
                next_state = self.game.board
                action = column
                current_player_agent.update_q_table(current_state, action, reward, next_state, done)

            if winner:
                self.handle_game_over(winner)
            elif self.game.is_full():
                self.handle_game_over(None)

            # Check so that the AI automatically plays after the previous player
            if self.player1_algorithm is not None and self.game.current_player == 1:
                # Recursive call so that the AI plays automatically after a one-second pause
                self.master.after(100, self.drop_piece, None)
            if self.player2_algorithm is not None and self.game.current_player == 2:
                # Recursive call so that the AI plays automatically after a one-second pause
                self.master.after(100, self.drop_piece, None)


    """Handles the end of the game."""
    def handle_game_over(self, winner):
        if winner:
            win_text = f"Player {winner} won !"
        else:
            win_text = "Draw !"

        self.display_game_over_message(win_text)


    """Displays a message when the game is over."""
    def display_game_over_message(self, message):
        restart = tk.messagebox.askyesno("Restart", message + " Would you like to start a new game?")
        if restart:
            self.game.reset_board()
            self.update_board()
        else:
            self.close()

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

    """Calculates the reward for the current player. Only used for reinforcement learning."""
    def calculate_reward_qLearning(self, winner, done):
        if winner == self.game.current_player:
            # Reward to win
            return 1
        elif done:
            # Neutral reward for a draw
            return 0
        else:
            # Small penalty to continue play
            return -0.1


def main():
    root = tk.Tk()
    gui = ConnectFourGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
