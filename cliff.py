import numpy as np

BOARD_ROWS = 4
BOARD_COLS = 12
WIN_STATE = (3, 11)
START = (3, 0)


class Cliff:
    def __init__(self):
        self.end = False
        self.pos = START
        self.board = np.zeros([4, 12])
        self.board[3, 1:11] = -1

    def next_pos(self, act):
        if act == "up":
            nxt_pos = (self.pos[0] - 1, self.pos[1])
        elif act == "down":
            nxt_pos = (self.pos[0] + 1, self.pos[1])
        elif act == "left":
            nxt_pos = (self.pos[0], self.pos[1] - 1)
        else:
            nxt_pos = (self.pos[0], self.pos[1] + 1)

        if 0 <= nxt_pos[0] <= 3:
            if 0 <= nxt_pos[1] <= 11:
                self.pos = nxt_pos

        if self.pos == WIN_STATE:
            self.end = True
            print("Game ends reaching goal")

        if self.board[self.pos] == -1:
            self.end = True
            print("Game ends falling off cliff")

        return self.pos

    def get_reward(self):
        if self.pos == WIN_STATE:
            return -1
        if self.board[self.pos] == 0:
            return -1
        return -100

    def show(self):
        for i in range(0, BOARD_ROWS):
            print("-------------------------------------------------")
            out = "| "
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == -1:
                    token = "*"
                if self.board[i, j] == 0:
                    token = "0"
                if (i, j) == self.pos:
                    token = "S"
                if (i, j) == WIN_STATE:
                    token = "G"
                out += token + " | "
            print(out)
        print("-------------------------------------------------")
