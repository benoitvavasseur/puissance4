import tkinter as tk
from package.gui import ConnectFourGUI
from package.optimization.minMax import MiniMaxAlgorithm
from package.reinforcement.qLearning import QLearningAlgorithm

# Agent type configuration
PLAYER1_TYPE = "QLEARNING"  # Options: "QLEARNING", "MINMAX", "HUMAN"
PLAYER2_TYPE = "QLEARNING"  # Options: "QLEARNING", "MINMAX", "HUMAN"

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
    else:
        return None  # No agent for a human player

def main():
    root = tk.Tk()

    player1_agent = create_agent(PLAYER1_TYPE, 1)
    player2_agent = create_agent(PLAYER2_TYPE, 2)

    gui = ConnectFourGUI(root, player1_algorithm=player1_agent, player2_algorithm=player2_agent)

    if isinstance(player1_agent, QLearningAlgorithm):
        gui.add_on_close_callback(lambda: player1_agent.save_q_table("package/reinforcement/q_table_player1.json"))

    if isinstance(player2_agent, QLearningAlgorithm):
        gui.add_on_close_callback(lambda: player2_agent.save_q_table("package/reinforcement/q_table_player2.json"))

    root.protocol("WM_DELETE_WINDOW", gui.close)
    root.mainloop()

if __name__ == "__main__":
    main()
