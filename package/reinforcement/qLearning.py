import json

import numpy as np

class QLearningAlgorithm:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}  # initialise with an empty table or load a pre-existing table

    """Returns the next move to play."""
    def get_next_move(self, board_state, available_columns):
        state = self._board_to_state(board_state)
        if np.random.uniform(0, 1) < self.epsilon:
            # Random selection from available columns
            return np.random.choice(available_columns)
        else:
            # Select the best action from the available columns
            return self._best_action(state, available_columns)

    """Updates the Q table based on the result of the last action."""
    def update_q_table(self, current_state, action, reward, next_state, done):
        # Converts the state into a string for use as a key in table Q
        current_state_key = str(current_state)
        next_state_key = str(next_state)

        # Initializes Q values if the state is not yet in the table
        if current_state_key not in self.q_table:
            self.q_table[current_state_key] = np.zeros(7)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(7)

        # Update table Q
        old_value = self.q_table[current_state_key][action]
        next_max = np.max(self.q_table[next_state_key])

        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max * (1 - int(done)))
        self.q_table[current_state_key][action] = new_value

    """Returns the best action to take from the given state."""
    def _best_action(self, state, available_columns):
        state_key = str(state)
        if state_key in self.q_table:
            # Create a filter for available actions
            action_filter = [i for i in range(7) if i in available_columns]

            # Apply the filter to obtain the available actions and Q values
            filtered_actions = np.array(action_filter)
            filtered_q_values = np.array([self.q_table[state_key][i] for i in filtered_actions])

            # Select the action with the maximum Q value
            return filtered_actions[np.argmax(filtered_q_values)]
        else:
            return np.random.choice(available_columns)

    """Converts the board into a string."""
    def _board_to_state(self, board):
        # Converts the board into a string
        return str(board)

    """Saves the Q table in a JSON file."""
    def save_q_table(self, filename):
        print(f"Saving the Q table in {filename}")
        try:
            # Converts each numpy array into a list
            serializable_q_table = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in self.q_table.items()}

            with open(filename, "w") as file:
                json.dump(serializable_q_table, file)
        except Exception as e:
            print(f"Error saving file {filename}: {e}")


    """Loads the Q table from a JSON file."""
    def load_q_table(self, filename):
        print(f"Attempt to load the file: {filename}")
        try:
            with open(filename, "r") as file:
                self.q_table = json.load(file)
        except FileNotFoundError:
            print(f"The file {filename} does not exist. Initialisation of a new Q table.")
            self.q_table = {}
        except json.JSONDecodeError:
            print(f"Error reading JSON file {filename}. Initialising a new table Q.")
            self.q_table = {}
        except Exception as e:
            print(f"An unexpected error has occurred while reading the file {filename}: {e}")
            self.q_table = {}

