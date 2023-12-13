import tkinter as tk
from package.gui import ConnectFourGUI
from package.optimization.minMax import MiniMaxAlgorithm
from package.reinforcement.qLearning import QLearningAlgorithm
from package.supervised.MonteCarloTree import MonteCarloTreeSearch

# Agent type configuration
PLAYER1_TYPE = "MONTECARLO"  # Options: "QLEARNING", "MONTECARLO", "MINMAX", "HUMAN"
PLAYER2_TYPE = "MINMAX"  # Options: "QLEARNING", "MONTECARLO", "MINMAX", "HUMAN"
NUM_GAMES = 1

"""Selects the type of agents to play the game"""
def select_agent_types():
    def submit():
        global PLAYER1_TYPE, PLAYER2_TYPE, NUM_GAMES
        PLAYER1_TYPE = player1_var.get()
        PLAYER2_TYPE = player2_var.get()
        NUM_GAMES = int(num_games_entry.get())
        selection_window.destroy()

    selection_window = tk.Tk()
    selection_window.title("Select agents")

    # Number of games
    num_games_entry = tk.Entry(selection_window)
    num_games_entry.pack()
    num_games_entry.insert(0, "1")

    # Center the window
    window_width = 300
    window_height = 150
    screen_width = selection_window.winfo_screenwidth()
    screen_height = selection_window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    selection_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    # Player selection
    player1_var = tk.StringVar(value="QLEARNING")
    player2_var = tk.StringVar(value="MINMAX")

    tk.Label(selection_window, text="Player 1:").pack()
    tk.OptionMenu(selection_window, player1_var, "QLEARNING", "MINMAX", "MONTECARLO", "HUMAN").pack()

    tk.Label(selection_window, text="Player 2:").pack()
    tk.OptionMenu(selection_window, player2_var, "QLEARNING", "MINMAX", "MONTECARLO", "HUMAN").pack()

    tk.Button(selection_window, text="START", command=submit).pack()

    selection_window.mainloop()
    return PLAYER1_TYPE, PLAYER2_TYPE, NUM_GAMES

"""Creates the 2 agents."""""
def create_agent(agent_type, player_number):
    if agent_type == "QLEARNING":
        agent = QLearningAlgorithm()
        try:
            agent.load_q_table(f"package/reinforcement/q_table_player{player_number}.json")
        except FileNotFoundError:
            pass
        return agent
    elif agent_type == "MINMAX":
        return MiniMaxAlgorithm()
    elif agent_type == "MONTECARLO":
        return MonteCarloTreeSearch()
    else:
        return None

""" Main function """
def main():
    player1_type, player2_type, num_games = select_agent_types()

    root = tk.Tk()

    player1_agent = create_agent(player1_type, 1)
    player2_agent = create_agent(player2_type, 2)

    gui = ConnectFourGUI(root, player1_algorithm=player1_agent, player2_algorithm=player2_agent, num_games=num_games)

    if isinstance(player1_agent, QLearningAlgorithm):
        gui.add_on_close_callback(lambda: player1_agent.save_q_table("package/reinforcement/q_table_player1.json"))

    if isinstance(player2_agent, QLearningAlgorithm):
        gui.add_on_close_callback(lambda: player2_agent.save_q_table("package/reinforcement/q_table_player2.json"))

    root.protocol("WM_DELETE_WINDOW", gui.close)
    root.mainloop()

if __name__ == "__main__":
    main()
