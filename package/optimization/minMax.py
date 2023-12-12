# minMax.py

MAX_DEPTH = 3


class MiniMaxAlgorithm:

    def get_next_move(self, board):
        best_score = float('-inf')
        best_move = None

        for move in self.get_possible_moves(board):
            temp_board = self.make_move(board, move, 1)
            score = self.minimax(temp_board, 0, False)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, board, depth, is_maximizing):
        if self.is_terminal_node(board) or depth == MAX_DEPTH:
            return self.evaluate_board(board, depth)

        if is_maximizing:
            best_score = float('-inf')
            for move in self.get_possible_moves(board):
                temp_board = self.make_move(board, move, 1)
                score = self.minimax(temp_board, depth + 1, False)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_possible_moves(board):
                temp_board = self.make_move(board, move, 2)
                score = self.minimax(temp_board, depth + 1, True)
                best_score = min(best_score, score)
            return best_score

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

    def evaluate_board(self, board, depth):
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
