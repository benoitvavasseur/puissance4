import random


class ConnectFourGame:
    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.moves = []

    """Returns True if the piece was successfully dropped, False otherwise."""
    def drop_piece(self, column):
        if column is None:
            available_columns = [i for i in range(7) if self.board[0][i] == 0]
            if not available_columns:
                return False  # Aucun mouvement possible
            column = random.choice(available_columns)
        for row in reversed(range(6)):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                self.moves.append((self.current_player, column))
                if not self.check_winner():
                    self.switch_player()
                return True
        return False

    def get_all_moves(self):
        return self.moves

    """Switches the current player."""
    def switch_player(self):
        self.current_player = 3 - self.current_player

    """ Returns the winner if there is one, None otherwise. """
    def check_winner(self):
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == self.current_player and all(self.board[row][col+i] == self.current_player for i in range(4)):
                    return self.current_player

        for col in range(7):
            for row in range(3):
                if self.board[row][col] == self.current_player and all(self.board[row+i][col] == self.current_player for i in range(4)):
                    return self.current_player

        for col in range(4):
            for row in range(3, 6):
                if self.board[row][col] == self.current_player and all(self.board[row-i][col+i] == self.current_player for i in range(4)):
                    return self.current_player

        for col in range(4):
            for row in range(3):
                if self.board[row][col] == self.current_player and all(self.board[row+i][col+i] == self.current_player for i in range(4)):
                    return self.current_player
        return None

    """Returns True if the board is full, False otherwise."""
    def is_full(self):
        return all(self.board[0][col] != 0 for col in range(7))

    """Resets the board."""
    def reset_board(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.moves = []