import numpy as np


class QTable:
    def __init__(self):
        self.actions = ["up", "right", "left", "down"]
        self.states = ["start", "end", "cliff", "idle"]
        self.qTable = np.zeros([4, 4])

    def show(self):
        print(self.qTable)
