from qAlgo import QLearning
from qTable import QTable
from board import Board

if __name__ == "__main__":
    board = Board()

    qTable = QTable(board)
    qTable.init_QTable()
    qTable.show()

    qLearning = QLearning(qTable)
