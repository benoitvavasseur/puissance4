# gui.py
import tkinter as tk
from tkinter import messagebox

from package.reinforcement.qLearning import QLearningAlgorithm
from .game import ConnectFourGame
import time

class ConnectFourGUI:
    def __init__(self, master, player1_algorithm=None, player2_algorithm=None, num_games=1):
        self.master = master
        self.master.title("Connect 4")
        self.game = ConnectFourGame()
        self.player1_algorithm = player1_algorithm
        self.player2_algorithm = player2_algorithm
        self.buttons = [tk.Button(self.master, text="Drop", command=lambda col=i: self.drop_piece(col)) for i in range(7)]
        self.create_widgets()
        self.on_close_callbacks = []
        self.num_games = num_games
        self.games_played = 0

        # Initiates the first move if both players are AIs
        if self.player1_algorithm is not None and self.player2_algorithm is not None:
            self.master.after(1000, lambda: self.drop_piece(None))

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
            print(f"drop_piece called for column {column}")

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
                self.master.after(500, self.drop_piece, None)
            if self.player2_algorithm is not None and self.game.current_player == 2:
                # Recursive call so that the AI plays automatically after a one-second pause
                self.master.after(500, self.drop_piece, None)


    """Handles the end of the game."""
    def handle_game_over(self, winner):
        print(f"Game over. Winner: {winner}")

        # Displays a message based on the result
        if winner:
            win_text = f"Player {winner} won!"
        else:
            win_text = "It's a draw!"

        # If at least one of the players is human
        if self.player1_algorithm is None or self.player2_algorithm is None:
            # Displays the end-of-game message and asks if they want to play again
            self.display_game_over_message(win_text)
        else:
            # Increments the games played counter
            self.games_played += 1

            # If both players are AIs, check whether the number of games played is less than the total number of games to be played
            if self.games_played < self.num_games:
                # Resets the board for a new game
                self.game.reset_board()
                self.update_board()

                # Automatically start the next game
                print("Scheduling next game in 2 seconds...")
                self.master.after(2000, lambda: self.drop_piece(None))
            else:
                # If all the games have been played, close the application
                print("All games played. Closing application.")
                self.close()

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
        self.master.update_idletasks() #lorsque deux minmax jouent plusieurs parties, le canvas ne se met pas à jour sans


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
