import streamlit as st
import numpy as np

st.title("Rock Paper Scissors - CFR Bot")

ACTIONS = ["Rock", "Paper", "Scissors"]
NUM_ACTIONS = 3

# CFR code simplified
class CFR:
    def __init__(self):
        self.regret_sum = np.zeros(NUM_ACTIONS)
        self.strategy_sum = np.zeros(NUM_ACTIONS)

    def get_average_strategy(self):
        norm = self.strategy_sum.sum()
        return self.strategy_sum / norm if norm > 0 else np.ones(NUM_ACTIONS) / NUM_ACTIONS

    def train(self, iterations):
        strategy = np.ones(NUM_ACTIONS) / NUM_ACTIONS
        for _ in range(iterations):
            utility = np.zeros(NUM_ACTIONS)
            for a in range(NUM_ACTIONS):
                for b in range(NUM_ACTIONS):
                    if a == b: utility[a] += 0
                    elif (a - b) % 3 == 1: utility[a] += 1
                    else: utility[a] -= 1
            expected = np.dot(utility, strategy)
            for a in range(NUM_ACTIONS):
                self.regret_sum[a] += utility[a] - expected
            strategy = np.maximum(self.regret_sum, 0)
            strategy = strategy / strategy.sum() if strategy.sum() > 0 else np.ones(NUM_ACTIONS) / NUM_ACTIONS
            self.strategy_sum += strategy

cfr = CFR()
cfr.train(10000)
bot_strategy = cfr.get_average_strategy()

user_choice = st.radio("Choose your move:", ACTIONS)
if st.button("Play"):
    user_index = ACTIONS.index(user_choice)
    bot_move = np.random.choice(NUM_ACTIONS, p=bot_strategy)
    result = "Tie" if user_index == bot_move else ("You Win!" if (user_index - bot_move) % 3 == 1 else "Bot Wins!")
    st.write(f"You chose {ACTIONS[user_index]}, Bot chose {ACTIONS[bot_move]}")
    st.success(result)
