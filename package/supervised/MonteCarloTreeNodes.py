import random
import math


class MonteCarloTreeNodes:
    def __init__(self, board, move=None, parent=None, player=1, historical_data=None):
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self.get_possible_moves(board)
        self.player = player
        self.historical_data = historical_data

    @staticmethod
    def copy_board(board):
        return [row[:] for row in board]

    def get_possible_moves(self, board):
        return [col for col in range(len(board[0])) if board[0][col] == 0]

    def select_child(self):
        selected_child = None
        historical_bias = 0.15  # Adjust this value depending on the accuracy of the game in the game_history.json
        best_value = -float('inf')
        for child in self.children:
            ucb1_value = self.calculate_ucb1(child)
            if child.move in self.historical_data:
                ucb1_value += self.historical_data[child.move] * historical_bias
            if ucb1_value > best_value:
                selected_child = child
                best_value = ucb1_value
        return selected_child

    def calculate_ucb1(self):
        exploration_param = math.sqrt(2)
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + exploration_param * math.sqrt(math.log(self.parent.visits) / self.visits)

    def expand(self):
        # Only expand if there are untried moves left
        if self.untried_moves:
            move = random.choice(self.untried_moves)
            self.untried_moves.remove(move)  # Or you can choose randomly
            new_board, _ = self.play_move(self.board, move, self.player)  # This method must return the new board state

            # Ensure that new_board is not None and is a valid board state before proceeding
            if new_board:
                new_node = MonteCarloTreeNodes(new_board, move=move, parent=self, player=3 - self.player,
                                               historical_data=self.historical_data)
                self.children.append(new_node)

            # Debugging: Print all children after expansion
            print(f"Children after expansion: {[child.move for child in self.children]}")

        return self

    def simulate(self):
        current_state, current_player = self.board, self.player

        while True:
            possible_moves = self.get_possible_moves(current_state)

            if not possible_moves:
                return 0

            move = random.choice(possible_moves)
            new_state, next_player = self.play_move(current_state, move, current_player)

            if next_player is None:
                if self.is_winner(new_state, current_player):
                    return current_player
                else:
                    return 0

            new_state_tuple = self.play_move(current_state, move, current_player)
            new_board_state, next_player = new_state_tuple

            current_state = MonteCarloTreeNodes.copy_board(new_board_state)
            current_player = next_player

    def update(self, result):
        self.visits += 1
        if self.player == result:
            self.wins += 1

    def play_move(self, board, column, player):
        new_board = MonteCarloTreeNodes.copy_board(board)

        # Check if the move is valid (column is not full)
        if new_board[0][column] != 0:
            # Invalid move (column is full), return the board as is and the same player
            return board, player

        # Find the first empty space in the column and place the player's piece
        for row in range(5, -1, -1):  # Start from the bottom of the board
            if new_board[row][column] == 0:
                new_board[row][column] = player
                break

        # After a move, check for a win or a draw before switching players
        if self.check_for_win(player) or self.is_board_full():
            # Game over, no need to switch players
            return new_board, None

        # Determine the next player and return the updated state
        next_player = 3 - player
        return new_board, next_player

        # Return the updated board state and the next player
        return new_board, next_player

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal_node(self):
        # A node is terminal if there is a win or if the board is full (draw)
        return self.check_for_win(self.player) or self.is_board_full()

    def check_for_win(self, player):
        # Check horizontal, vertical, and diagonal lines for a win
        board = self.board
        # Define the number of rows and columns
        ROWS, COLS = len(board), len(board[0])

        # Check horizontal lines
        for row in range(ROWS):
            for col in range(COLS - 3):
                if all(board[row][col + i] == player for i in range(4)):
                    return True

        # Check vertical lines
        for col in range(COLS):
            for row in range(ROWS - 3):
                if all(board[row + i][col] == player for i in range(4)):
                    return True

        # Check for positive diagonal lines
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                if all(board[row + i][col + i] == player for i in range(4)):
                    return True

        # Check for negative diagonal lines
        for row in range(3, ROWS):
            for col in range(COLS - 3):
                if all(board[row - i][col + i] == player for i in range(4)):
                    return True

        # If no win condition is met
        return False

    def is_board_full(self):
        # Check if all cells in the board are filled (i.e., no more moves possible)
        return all(cell != 0 for row in self.board for cell in row)

    def is_winner(self, board, player):
        # Check for horizontal, vertical, and diagonal wins
        for row in range(6):
            for col in range(7):
                # Check horizontal
                if col <= 3 and all(board[row][col + i] == player for i in range(4)):
                    return True
                # Check vertical
                if row <= 2 and all(board[row + i][col] == player for i in range(4)):
                    return True
                # Check for positive diagonal
                if row <= 2 and col <= 3 and all(board[row + i][col + i] == player for i in range(4)):
                    return True
                # Check for negative diagonal
                if row >= 3 and col <= 3 and all(board[row - i][col + i] == player for i in range(4)):
                    return True
        return False

    def backpropagate(self, result):
        # Increment the visit count for this node
        self.visits += 1
        if self.player == result:
            self.wins += 1

        # Debugging: Print the current node's stats after backpropagation
        print(
            f"Backpropagating node: Move = {self.move}, Player = {self.player}, Wins = {self.wins}, Visits = {self.visits}")

        # Recursive backpropagation
        if self.parent:
            self.parent.backpropagate(result)

    def get_best_child(self, exploration_weight=math.sqrt(2)):
        best_score = -float('inf')
        best_child = None

        for child in self.children:
            exploitation_score = child.wins / child.visits if child.visits > 0 else 0
            exploration_score = math.sqrt(math.log(self.visits) / child.visits) if child.visits > 0 else float('inf')
            uct_score = exploitation_score + exploration_weight * exploration_score

            if uct_score > best_score:
                best_score = uct_score
                best_child = child

        return best_child
