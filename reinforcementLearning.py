from qAgent import QAgent
from board import Board

if __name__ == "__main__":
    board = Board()
    agent = QAgent(board)

    EPISODES = 100

    for _ in range(EPISODES):
        agent.train()

    agent.print_qTable()
    board.show(agent.get_path())
