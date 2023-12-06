# optimization/minMax.py
from package.game import ConnectFourGame

class MiniMaxAlgorithm:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

    def get_next_move(self, board):
        best_move, _ = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True)
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal_node(board):
            return None, self.evaluate_board(board)

        valid_moves = [col for col in range(7) if board[0][col] == 0]

        if maximizing_player:
            value = float('-inf')
            best_move = None
            for move in valid_moves:
                new_board = self.make_move(board, move, 1)  # Assuming 1 is the maximizing player
                score = self.minimax(new_board, depth - 1, alpha, beta, False)[1]
                if score > value:
                    value = score
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_move, value
        else:
            value = float('inf')
            best_move = None
            for move in valid_moves:
                new_board = self.make_move(board, move, 2)  # Assuming 2 is the minimizing player
                score = self.minimax(new_board, depth - 1, alpha, beta, True)[1]
                if score < value:
                    value = score
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_move, value

    def is_terminal_node(self, board):
        connect_four_game = ConnectFourGame()
        connect_four_game.board = board  # Mettez à jour le plateau de jeu de l'instance
        return connect_four_game.check_winner() or self.is_board_full(board)

    def evaluate_board(self, board):
        winner = ConnectFourGame().check_winner()
        if winner == 1:
            return 1  # Player 1 wins
        elif winner == 2:
            return -1  # Player 2 wins
        else:
            return 0  # Draw

    def is_board_full(self, board):
        return all(board[0][col] != 0 for col in range(7))

    def make_move(self, board, column, player):
        new_board = [row[:] for row in board]
        connect_four_game = ConnectFourGame()
        connect_four_game.drop_piece(column)
        return connect_four_game.board
