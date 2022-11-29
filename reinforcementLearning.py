from qTable import QTable
from cliff import Cliff

if __name__ == "__main__":
    cliff = Cliff()
    cliff.show()
    cliff.next_pos("right")
    print(cliff.get_reward())

    qTable = QTable()
    qTable.show()
