# main.py
from package.gui import ConnectFourGUI
from package.optimization.minMax import MiniMaxAlgorithm
import tkinter as tk

def main():
    root = tk.Tk()
    #Player human : player_algorithm=None
    #Player MinMaxAlgorithm : player_algorithm=MiniMaxAlgorithm()

    # Example : Player vs. MiniMax
    gui_player_vs_minimax = ConnectFourGUI(root, player1_algorithm=MiniMaxAlgorithm(), player2_algorithm=MiniMaxAlgorithm())
    gui_player_vs_minimax.master.mainloop()

if __name__ == "__main__":
    main()
