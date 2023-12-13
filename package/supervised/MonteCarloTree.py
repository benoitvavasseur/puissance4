import puissance4
import MonteCarloTreeNodes


class MonteCarloTreeSearch:
    def __init__(self, c=1.4, number_of_iterations=1500):
        self.root = None
        self.c = c  # exploration parameter
        self.number_of_iterations = number_of_iterations

    def best_move(self, game_state):
        self.root = MonteCarloTreeNodes(game_state)

        for _ in range(self.number_of_iterations):
            node = self.select(self.root)  # selection
            score = self.simulate(node.game_state)  # simulation
            self.backpropagate(node, score)  # backpropagation

        # return the move that leads to the child with the best score
        return self.get_best_move()
    # ... additional methods ...
