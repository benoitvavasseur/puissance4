class MonteCarloTreeNodes:
    # Node for MCTS tree
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0