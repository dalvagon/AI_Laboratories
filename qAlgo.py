class QLearning:
    def __init__(self, qTable):
        self.LEARNING_RATE = 0.9
        self.DISCOUNT = 1
        self.qTable = qTable
