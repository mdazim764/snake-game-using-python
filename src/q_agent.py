import numpy as np
import random
import pickle
import os

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=1.0, epsilon_decay=0.99, epsilon_min=0.01):
        self.lr = learning_rate          # Learning rate (alpha)
        self.gamma = discount_factor     # Discount factor for future rewards
        self.epsilon = epsilon           # Exploration rate (shuru me 100% random exploration)
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        # Q-Table: Dictionary mapping state_tuple -> [Q_straight, Q_right, Q_left]
        self.q_table = {}

    def get_q_values(self, state):
        """Agar state pehli baar aayi hai toh Q-table me [0, 0, 0] initialize karo"""
        if state not in self.q_table:
            self.q_table[state] = np.zeros(3)
        return self.q_table[state]

    def get_action(self, state, train_mode=True):
        """
        Epsilon-Greedy Policy:
        Training ke waqt epsilon probability se random action lega (Exploration),
        warna Q-table se best action chunega (Exploitation).
        """
        if train_mode and random.random() < self.epsilon:
            return random.randint(0, 2)
        
        q_vals = self.get_q_values(state)
        return int(np.argmax(q_vals))

    def learn(self, state, action, reward, next_state, done):
        """Bellman Equation se Q-value update karta hai"""
        old_q = self.get_q_values(state)[action]
        
        if done:
            next_max = 0.0  # Terminal state ke baad koi future reward nahi hota
        else:
            next_max = np.max(self.get_q_values(next_state))

        # Temporal Difference calculation
        temporal_difference = reward + (self.gamma * next_max) - old_q
        
        # Update Q-table
        self.q_table[state][action] = old_q + (self.lr * temporal_difference)

    def decay_epsilon(self):
        """Har episode ke baad random exploration kam karta hai"""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, filename="q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.q_table, f)
        print(f"[SUCCESS] Trained Q-Table saved to '{filename}' (Total States Learned: {len(self.q_table)})")

    def load_model(self, filename="q_table.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                self.q_table = pickle.load(f)
            self.epsilon = 0.0  # Trained model me random exploration band
            print(f"[SUCCESS] Loaded Q-Table from '{filename}' ({len(self.q_table)} states)")
            return True
        return False