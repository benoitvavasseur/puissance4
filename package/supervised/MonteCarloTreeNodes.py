import random
import math


class MonteCarloTreeNodes:
    def __init__(self, board, move=None, parent=None, player=1):
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self.get_possible_moves(board)
        self.player = player  # The player who has just moved

    @staticmethod
    def copy_board(board):
        return [row[:] for row in board]
    def get_possible_moves(self, board):
        # Assume that the board is a list of lists, and that a 0 indicates an empty cell
        return [col for col in range(len(board[0])) if board[0][col] == 0]

    def select_child(self):
        # Select a child node using UCB1 formula
        selected_child = None
        best_value = -float('inf')
        for child in self.children:
            # Calculate the UCB1 value
            ucb1_value = child.wins / child.visits + math.sqrt(2) * math.sqrt(math.log(self.visits) / child.visits)
            if ucb1_value > best_value:
                selected_child = child
                best_value = ucb1_value
        return selected_child

    def expand(self):
        # Take a move from the untried moves, play it on the board, and add a new node to the children
        move = self.untried_moves.pop()
        new_board = MonteCarloTreeNodes.copy_board(
            self.board)  # Assume that this function makes a move on the board and returns the new board
        new_node = MonteCarloTreeNodes(new_board, move=move, parent=self, player=3 - self.player)
        self.children.append(new_node)
        return new_node

    def simulate(self,  max_depth=100):
        # Copy the current state to avoid modifying the original board
        current_state = MonteCarloTreeNodes.copy_board(self.board)
        current_player = self.player

        while True:
            # Get all possible moves for the current state
            possible_moves = self.get_possible_moves(current_state)

            # If there are no possible moves, it's a draw
            if not possible_moves:
                return 0  # Return 0 or another value that signifies a draw

            # Randomly select one of the possible moves
            move = random.choice(possible_moves)

            # Play the move and get the new state
            new_state, next_player = self.play_move(current_state, move, current_player)

            # If there's no next player, the game is over
            if next_player is None:
                if self.is_winner(new_state, current_player):
                    return current_player  # Current player won
                else:
                    return 0  # It's a draw

            # If the game isn't over, prepare for the next iteration
            current_state = new_state
            current_player = next_player

    def update(self, result):
        # Update this node's data based on the simulation result
        self.visits += 1
        if self.player == result:
            self.wins += 1

    def play_move(self, board, column, player):
        # Deep copy the board to avoid modifying the original
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

        # If the result of the simulation is a win for this node's player, increment the win count
        if result == self.player:
            self.wins += 1

        # If there's a parent node, recursively backpropagate the result up the tree
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