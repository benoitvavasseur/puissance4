import json

from puissance4.package.supervised.MonteCarloTreeNodes import MonteCarloTreeNodes
from copy import deepcopy
import time


class MonteCarloTreeSearch:
    def __init__(self, time_limit=1.0, iteration_limit=100):
        self.time_limit = time_limit
        self.iteration_limit = iteration_limit
        self.start_time = None
        self.historical_data = self.load_historical_data()

    def load_historical_data(self):
        try:
            with open("game_history.json", "r") as file:
                historical_data = json.load(file)
        except FileNotFoundError:
            return {}
        return self.analyze_historical_data(historical_data)

    def analyze_historical_data(self, raw_data):
        winning_moves = {}
        for game in raw_data:
            if game["winner"]:
                for move in game["moves"]:
                    if move[0] == game["winner"]:
                        winning_moves[move[1]] = winning_moves.get(move[1], 0) + 1
        return winning_moves

    def get_next_move(self, board, available_columns=None):
        current_player = self.determine_current_player(board)
        self.start_time = time.time()
        root = MonteCarloTreeNodes(deepcopy(board), player=current_player, historical_data=self.historical_data)
        iterations = 100

        while self.time_limit_not_reached() and self.iteration_limit_not_reached(iterations):
            node = self.select_node(root)
            if node is None:
                break

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
        selected_child = None
        best_value = -float('inf')

        if not node.children:
            return node

        for child in node.children:
            ucb1_value = child.calculate_ucb1()
            if child.move in self.historical_data:
                ucb1_value += self.historical_data[child.move]
            if ucb1_value > best_value:
                selected_child = child
                best_value = ucb1_value
        return selected_child

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
