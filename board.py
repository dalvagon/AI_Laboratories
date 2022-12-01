import numpy as np


class Board:
    def __init__(self):
        self.BOARD_ROWS = 4
        self.BOARD_COLS = 12
        self.WIN_STATE = (3, 11)
        self.START = (3, 0)

        self.end = False
        self.pos = self.START
        self.cells = [
            [0 for _ in range(self.BOARD_COLS)] for _ in range(self.BOARD_ROWS)
        ]
        for col in range(1, 11):
            self.cells[3][col] = -1

    def get_next_pos(self, pos, act):
        if act == "up":
            nxt_pos = (pos[0] - 1, pos[1])
        elif act == "down":
            nxt_pos = (pos[0] + 1, pos[1])
        elif act == "left":
            nxt_pos = (pos[0], pos[1] - 1)
        else:
            nxt_pos = (pos[0], pos[1] + 1)

        if 0 <= nxt_pos[0] <= self.BOARD_ROWS - 1:
            if 0 <= nxt_pos[1] <= self.BOARD_COLS - 1:
                return nxt_pos

    def set_next_pos(self, act):
        nxt_pos = self.get_next_pos(act)

    def get_reward(self, pos):
        if pos == None:
            return None

        if pos == self.WIN_STATE:
            return 0

        if self.cells[pos[0]][pos[1]] == 0:
            return -1

        return -100

    def show(self):
        for i in range(0, self.BOARD_ROWS):
            print("-------------------------------------------------")
            out = "| "
            for j in range(0, self.BOARD_COLS):
                if self.cells[i][j] == -1:
                    token = "*"
                if self.cells[i][j] == 0:
                    token = "0"
                if (i, j) == self.pos:
                    token = "S"
                if (i, j) == self.WIN_STATE:
                    token = "W"
                out += token + " | "
            print(out)
        print("-------------------------------------------------")
