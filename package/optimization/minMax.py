# minMax.py

MAX_DEPTH = 5


class MiniMaxAlgorithm:
    """Returns the value of the column where MinMax should play"""
    def get_next_move(self, board):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        for move in self.get_possible_moves(board):
            temp_board = self.make_move(board, move, 1)
            score = self.minimax(temp_board, 0, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    """MinMax algorithm: explores the branches of the decision tree to deduce the best score"""
    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if self.is_terminal_node(board) or depth == MAX_DEPTH:
            return self.evaluate_board(board, depth)

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_possible_moves(board):
                temp_board = self.make_move(board, move, 1)
                eval = self.minimax(temp_board, depth + 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(board):
                temp_board = self.make_move(board, move, 2)
                eval = self.minimax(temp_board, depth + 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    """Checks if a move is possible or not (full column)"""
    @staticmethod
    def get_possible_moves(board):
        return [c for c in range(7) if board[0][c] == 0]

    @staticmethod
    def make_move(board, column, player):
        temp_board = [row[:] for row in board]
        for row in reversed(range(6)):
            if temp_board[row][column] == 0:
                temp_board[row][column] = player
                break
        return temp_board

    """Checks if you have reached the end of the decision tree"""
    @staticmethod
    def is_terminal_node(board):
        # Utilise une logique similaire à check_winner de ConnectFourGame
        # Vérifie également si le plateau est plein
        for row in range(6):
            for col in range(4):
                if board[row][col] != 0 and all(board[row][col] == board[row][col + i] for i in range(4)):
                    return True

        for col in range(7):
            for row in range(3):
                if board[row][col] != 0 and all(board[row + i][col] == board[row][col] for i in range(4)):
                    return True

        for col in range(4):
            for row in range(3, 6):
                if board[row][col] != 0 and all(board[row - i][col + i] == board[row][col] for i in range(4)):
                    return True

        for col in range(4):
            for row in range(3):
                if board[row][col] != 0 and all(board[row + i][col + i] == board[row][col] for i in range(4)):
                    return True

        if all(board[0][col] != 0 for col in range(7)):  # Vérifie si le plateau est plein
            return True

        return False

    """Evaluate the board to return the score"""
    def evaluate_board(self, board, depth):
        if self.winning_move(board, 1):
            return 100000

        if self.winning_move(board, 2):
            return -100000
        score = 0
        score_center = 3
        score_3_align = 5 * (10 - depth)
        score_2_align = 2 * (10 - depth)



        center_array = [board[i][3] for i in range(6)]
        center_count = center_array.count(1)
        score += center_count * score_center

        for row in range(6):
            row_array = board[row]
            for col in range(4):
                window = row_array[col:col + 4]
                score += self.evaluate_window(window, score_3_align, score_2_align)

        for col in range(7):
            col_array = [board[row][col] for row in range(6)]
            for row in range(3):
                window = col_array[row:row + 4]
                score += self.evaluate_window(window, score_3_align, score_2_align)

        for row in range(3, 6):
            for col in range(4):
                window = [board[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window, score_3_align, score_2_align)

        for row in range(3):
            for col in range(4):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window, score_3_align, score_2_align)

        return score

    """Check if a player will win"""
    @staticmethod
    def winning_move(board, piece):
        # Constants for the board size
        ROW_COUNT = 6
        COLUMN_COUNT = 7

        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

        return False

    """Evaluates the window to know if a line is blocked by the edges or not"""
    @staticmethod
    def evaluate_window(window, score_3_align, score_2_align):
        score = 0
        if window.count(1) == 3 and window.count(0) == 1:
            score += score_3_align
        elif window.count(1) == 2 and window.count(0) == 2:
            score += score_2_align

        if window.count(2) == 3 and window.count(0) == 1:
            score -= score_3_align

        return score
