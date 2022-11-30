import numpy as np
from pprint import pprint


class QTable:
    def __init__(self, board):
        self.actions = ["up", "right", "down", "left"]
        self.board = board
        self.qTable = {}

    def init_QTable(self):
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[0])):
                self.qTable[(row, col)] = [
                    self.board.get_reward(nxt_pos)
                    for nxt_pos in [
                        self.board.get_next_pos(
                            (row, col), action
                        )  # gets the positions obtainied by applying actions to (row, col)
                        for action in self.actions
                    ]
                ]

    def show(self):
        pprint(self.qTable)
