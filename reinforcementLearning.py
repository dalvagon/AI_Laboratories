from numpy import array
from qAgent import QAgent
from board import Board
import matplotlib.pyplot as plt

if __name__ == "__main__":
    board = Board()
    agent = QAgent(board)

    EPISODES = 100

    rewards = []
    for _ in range(EPISODES):
        reward = agent.train()
        rewards.append(reward)

    plt.plot(array(rewards))
    plt.show()

    agent.print_qTable()
    board.show(agent.get_path())
