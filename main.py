from package.gui import ConnectFourGUI
from package.optimization.minMax import MiniMaxAlgorithm
import tkinter as tk

from puissance4.package.supervised.MonteCarloTree import MonteCarloTreeSearch


def main():
    root = tk.Tk()

    #Player human : player_algorithm=None
    #Player MinMaxAlgorithm : player_algorithm=MiniMaxAlgorithm()
    #Player MonteCarloAlgorithm : player_algorithm=MonteCarloTree()

    minimax_algorithm = MiniMaxAlgorithm()
    monte_carlo_algorithm = MonteCarloTreeSearch(time_limit=1.0)

    # Example : MiniMaw vs MonteCarlo
    gui_minimax_vs_montecarlo = ConnectFourGUI(root, player1_algorithm=minimax_algorithm, player2_algorithm=monte_carlo_algorithm)
    gui_minimax_vs_montecarlo.master.mainloop()

    # Example : Player vs. MiniMax
    #gui_player_vs_minimax = ConnectFourGUI(root, player1_algorithm=MiniMaxAlgorithm(), player2_algorithm=MiniMaxAlgorithm())
    #gui_player_vs_minimax.master.mainloop()

if __name__ == "__main__":
    main()
