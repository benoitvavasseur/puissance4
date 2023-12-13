from package.supervised.MonteCarloTreeNodes import MonteCarloTreeNodes
from copy import deepcopy
import time


class MonteCarloTreeSearch:
    def __init__(self, time_limit=None, iteration_limit=None):
        self.time_limit = time_limit
        self.iteration_limit = iteration_limit
        self.start_time = None

    def get_next_move(self, board):
        current_player = self.determine_current_player(board)
        self.start_time = time.time()
        root = MonteCarloTreeNodes(deepcopy(board), player=current_player)

        iterations = 0
        while self.time_limit_not_reached() and self.iteration_limit_not_reached(iterations):
            node = self.select_node(root)
            winner = node.simulate()
            node.backpropagate(winner)
            iterations += 1

        return self.get_best_move(root)

    def time_limit_not_reached(self):
        if self.time_limit is None:
            return True
        return time.time() - self.start_time < self.time_limit

    def iteration_limit_not_reached(self, iterations):
        if self.iteration_limit is None:
            return True
        return iterations < self.iteration_limit

    def select_node(self, node):
        # Select a node that maximizes the UCT (Upper Confidence bounds applied to Trees) value
        while not node.is_terminal_node():
            if node.is_fully_expanded():
                node = node.get_best_child()
            else:
                return node.expand()
        return node

    def get_best_move(self, root):
        # Select the child with the highest win ratio
        best_win_ratio = -float('inf')
        best_move = None

        for child in root.children:
            win_ratio = child.wins / child.visits if child.visits > 0 else 0
            if win_ratio > best_win_ratio:
                best_win_ratio = win_ratio
                best_move = child.move

        return best_move

    def determine_current_player(self, board):
        # Logic to determine current player from board state
        # This is a placeholder; you will need to replace this with your own logic
        player1_count = sum(row.count(1) for row in board)
        player2_count = sum(row.count(2) for row in board)
        return 1 if player1_count <= player2_count else 2
